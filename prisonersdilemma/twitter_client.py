"""Module that implements a Twitter client for the Prisoner's Dilemma bot"""

import os
import json
import time
import logging
import argparse
from pathlib import Path
import tweepy
from dotenv import load_dotenv
import prisonersdilemma.strategy as strategy
from prisonersdilemma.bot import PrisonersDilemmaBot


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s\t%(levelname)s\t%(message)s",
    handlers=[logging.FileHandler("twitter_bot.log"), logging.StreamHandler()],
)

MESSAGES = dict(
    rules="""Let's play a game of Prisoner's Dilemma!

Reply with the move you want to play

▪️ COOPERATE, C or ✅
▪️ DEFECT, D or ❌

We'll be playing 10 rounds and I will assign the points like this:

✅ ✅ - 3 points each
❌ ❌ - 1 points each
✅ ❌ - 0 and 5 points respectively

Let's go!""",
    invalid_move="""Sorry I couldn't understand the move you want to play 😔

Please reply with one of the following:

▪️ COOPERATE, C or ✅
▪️ DEFECT, D or ❌""",
    game_update="""Game %d/%d

Your move: %s
My move: %s

You get %d points and I get %d points!

Current score:
▪️ You: %d points
▪️ Me: %d points

%s""",
    result_win="Congratulations! You won! 🥳",
    result_lose="Ha, you lost! 🤖",
    result_draw="Oh, I guess nobody wins this time... 🤷‍♂️",
    next_move="What is your next move?",
)


def get_end_game_message(points):
    """Get the end game message

    :param points: final points
    :return: text of the end game message
    """
    if points[0] < points[1]:
        return MESSAGES["result_win"]
    elif points[0] > points[1]:
        return MESSAGES["result_lose"]
    else:
        return MESSAGES["result_draw"]


def move_to_string(move):
    """Convert a Prisoner's Dilemma move to string"""
    return "✅" if move else "❌"


def parse_move(text):
    """Parse a Prisoner's Dilemma game move from text

    :param text: tex of the tweet containg the move
    :raises ValueError: raises an exception if no valid move can be found
    :return: True for COOPERATE and False for DEFECT
    """
    text = text.replace("@DilemmaBot", "").upper().strip()

    # Check for cooperate
    if "COOPERATE" in text:
        return True

    # Check for C
    if text == "C":
        return True

    # Check for cooperate emoji
    if "✅" in text:
        return True

    # Check for defect
    if "DEFECT" in text:
        return False

    # Check for D
    if text == "D":
        return False

    # Check for defect emoji
    if "❌" in text:
        return False

    # Raise exception if no valid move was found
    raise ValueError("No valid move found")


class PrisonersDilemmaTwitterClient:
    """Twitter client for the Prisoner's Dilemma bot"""

    def __init__(self, interval, state_file, active_games_file):
        """Initialize the Twitter Client"""
        logging.info("Starting the Prisoner's Dilemma Twitter Bot")

        # Init the object attributes
        self.interval = interval
        self.state_file = Path(state_file)
        self.active_games_file = Path(active_games_file)

        # Initilize the API
        logging.info("Initializing Twitter API")
        self.init_twitter_api()

        # Load the state
        logging.info("Loading the bot state from %s", state_file)
        self.load_state()

        # Initialize the bot
        self.bot = PrisonersDilemmaBot(strategy.play_tit_for_tat, moves_to_play=3)
        self.load_active_games()

    def init_twitter_api(self):
        """Authenticat and initilize the Twitter API

        :return: API obejct
        """
        auth = tweepy.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_SECRET"))
        auth.set_access_token(
            os.getenv("ACCESS_TOKEN"),
            os.getenv("ACCESS_TOKEN_SECRET"),
        )
        self.twitter_api = tweepy.API(auth)

    def load_state(self):
        """Load the state of the bot from a JSON file"""
        if self.state_file.exists():
            with open(self.state_file) as state_file_json:
                self.state = json.load(state_file_json)
        else:
            self.state = dict(last_status_id=0)

    def save_state(self):
        """Save the bot state to a file"""
        with open(self.state_file, "w") as state_file_json:
            return json.dump(self.state, state_file_json)

    def load_active_games(self):
        """Load the active games from a JSON file"""
        if self.active_games_file.exists():
            self.bot.load_active_games(self.active_games_file)

    def save_active_games(self):
        """Save the active games to a JSON file"""
        self.bot.save_active_games(self.active_games_file)

    def reply_to_tweet(self, text, tweet_id):
        """Reply to a tweet

        :param text: text of the reply
        :param id: ID of the tweet to reply to
        """
        try:
            self.twitter_api.update_status(
                text, in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True
            )
        except tweepy.error.TweepError:
            pass

    def process_tweet(self, tweet):
        """Process a single tweet

        :param tweet: Tweet mentioning the bot
        """
        user = tweet.user.screen_name
        # Check if the user starts a new game
        if not self.bot.is_user_playing(user):
            self.bot.play(user, True)
            self.reply_to_tweet(MESSAGES["rules"], tweet.id)
            return

        # Parse the move
        try:

            move = parse_move(tweet.text)
        except ValueError:
            self.reply_to_tweet(MESSAGES["invalid_move"], tweet.id)
            return

        # Play one round of the game
        game_state = self.bot.play(user, move)
        moves_played = len(game_state["moves"])
        last_moves = game_state["moves"][-1]

        # Check if the game is finished and prepare the message
        if moves_played == self.bot.moves_to_play:
            end_game_message = get_end_game_message(game_state["total_points"])
        else:
            end_game_message = MESSAGES["next_move"]

        # Reply to the tweet depending on the game state
        if moves_played == 0:
            self.reply_to_tweet(MESSAGES["rules"], tweet.id)
        else:
            self.reply_to_tweet(
                MESSAGES["game_update"]
                % (
                    moves_played,
                    self.bot.moves_to_play,
                    move_to_string(last_moves[1]),
                    move_to_string(last_moves[0]),
                    game_state["last_points"][1],
                    game_state["last_points"][0],
                    game_state["total_points"][1],
                    game_state["total_points"][0],
                    end_game_message,
                ),
                tweet.id,
            )

    def run(self):
        """Periodically search for new tweets and reply"""
        while True:
            logging.info("Searching for new tweets")
            tweets = self.twitter_api.search(
                "@DilemmaBot", since_id=self.state["last_status_id"]
            )
            logging.info("Found %d new tweets", len(tweets))

            for tweet in tweets:
                self.process_tweet(tweet)
                self.state["last_status_id"] = max(
                    tweet.id, self.state["last_status_id"]
                )

            self.save_state()
            self.save_active_games()

            time.sleep(args.interval)


def parse_args():
    """
    Configures the argument parser

    :return: Parsed arguments
    """

    description = """Twitter Bot that plays Prisoner's Dilemma"""

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "-i",
        "--interval",
        dest="interval",
        action="store",
        default=10.0,
        help="Time interval in seconds at which new tweets will be searched",
    )

    parser.add_argument(
        "-s",
        "--state",
        dest="state_file",
        action="store",
        default="twitter_bot_state.json",
        help="File storing the state of the bot",
    )

    parser.add_argument(
        "-g",
        "--games",
        dest="games_file",
        action="store",
        default="active_games.json",
        help="File storing the active games of the bot",
    )

    parser.add_argument(
        "-a",
        "--archive",
        dest="archive_file",
        action="store",
        default="archive.json",
        help="File storing the games that were finished as an archive",
    )

    return parser.parse_args()


if __name__ == "__main__":
    # Parse the arguments
    args = parse_args()

    # Create and run the Twitter client
    client = PrisonersDilemmaTwitterClient(
        args.interval, args.state_file, args.games_file
    )
    client.run()

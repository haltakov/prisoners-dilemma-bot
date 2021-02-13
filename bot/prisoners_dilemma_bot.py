import time
from bot.strategies import STRATEGIES


BOT_REPLIES = dict(
    rules="Hi, I'm the Prisoner's Dilemma Bot. We are going to play a game. Please reply with COOPERATE or DEFECT.",
    invalid_move="Sorry, I could't understand which move you want to play. Please reply with either COOPERATE (or just C) or DEFECT (or just D)",
)

MAX_TIME_TO_REPLY = 2  # days


class PrisonersDilemmaBot:
    def __init__(self, strategy="tit_for_tat", games_to_play=10):
        self.games_to_play = games_to_play
        self.active_games = {}
        self.strategy = STRATEGIES.get(strategy, STRATEGIES[list(STRATEGIES.keys())[0]])

    def play(self, user, text):
        # Get the active game
        game = self.active_games.get(user, None)

        # Check if there is no active game for this` user
        if not game:
            return self.start_new_game(user)

        # Check if a new game should be started, because the user didn't play for a long time
        if time.time() - game["last_time"] > MAX_TIME_TO_REPLY:
            return self.start_new_game(user)

        # Parse the other player's move
        try:
            move = self.parse_move(text)
        except ValueError:
            return BOT_REPLIES["invalid_move"]

    def start_new_game(self, user):
        self.active_games[user] = dict(start_time=time.time(), last_time=time.time())

        return BOT_REPLIES["rules"]

    def parse_move(self, text):
        # Check for cooperate
        if "COOPERATE" in text.upper():
            return True

        # Check for C
        if text.upper().strip() == "C":
            return True

        # Check for defect
        if "DEFECT" in text.upper():
            return False

        # Check for D
        if text.upper().strip() == "D":
            return False

        # Raise exception if no valid move was found
        raise ValueError("No valid move found")
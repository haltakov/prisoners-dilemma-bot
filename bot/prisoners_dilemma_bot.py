import time
from bot.strategies import STRATEGIES

BOT_REPLIES = dict(
    rules="Hi, I'm the Prisoner's Dilemma Bot. We are going to play a game. Please reply with COOPERATE or DEFECT.",
    invalid_move="Sorry, I could't understand which move you want to play. Please reply with either COOPERATE (or just C) or DEFECT (or just D)",
    game_update="Move %d out of %d\n\nYour move: %s\nMy move: %s\n\nYou get %d points and I get %d points\n\nTotal points count:\nYou: %d\nMe: %d\n\n%s",
    result_win="CONGRATILATIONS - You won!",
    result_lose="LOSER - You lost the game!",
    result_draw="The game is draw",
)

MAX_TIME_TO_REPLY = 2 * 86400  # 2 days


def get_end_game_message(points):
    if points[0] < points[1]:
        return BOT_REPLIES["result_win"]
    elif points[0] > points[1]:
        return BOT_REPLIES["result_lose"]
    else:
        return BOT_REPLIES["result_draw"]


def move_to_string(move):
    return "C" if move else "D"


class PrisonersDilemmaBot:
    def __init__(
        self, strategy="tit_for_tat", game_matrix=[5, 3, 1, 0], moves_to_play=10
    ):
        self.moves_to_play = moves_to_play
        self.game_matrix = game_matrix
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

        # Parse the opponent's move
        try:
            opponent_move = self.parse_move(text)
        except ValueError:
            return BOT_REPLIES["invalid_move"]

        # Play the move
        own_move = self.strategy(game["moves"])
        game["moves"].append((own_move, opponent_move))

        # Calculate the outcome and update the total points
        outcomes = self.get_outcomes(own_move, opponent_move)
        game["points"] = (
            game["points"][0] + outcomes[0],
            game["points"][1] + outcomes[1],
        )
        game["last_time"] = time.time()

        # Check if this is the last game and prepare the end game message
        moves_played = len(game["moves"])
        end_game_message = ""
        if moves_played == self.moves_to_play:
            end_game_message = get_end_game_message(game["points"])

        # Prepare the reply
        reply = BOT_REPLIES["game_update"] % (
            moves_played,
            self.moves_to_play,
            move_to_string(opponent_move),
            move_to_string(own_move),
            outcomes[1],
            outcomes[0],
            game["points"][1],
            game["points"][0],
            end_game_message,
        )

        # Delete the game if finished
        if moves_played == self.moves_to_play:
            del self.active_games[user]

        return reply

    def start_new_game(self, user):
        self.active_games[user] = dict(
            start_time=time.time(), last_time=time.time(), moves=[], points=(0, 0)
        )

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

    def get_outcomes(self, own_move, opponent_move):
        if own_move and opponent_move:
            return (self.game_matrix[1], self.game_matrix[1])
        elif not own_move and opponent_move:
            return (self.game_matrix[0], self.game_matrix[3])
        elif own_move and not opponent_move:
            return (self.game_matrix[3], self.game_matrix[0])
        else:
            return (self.game_matrix[2], self.game_matrix[2])

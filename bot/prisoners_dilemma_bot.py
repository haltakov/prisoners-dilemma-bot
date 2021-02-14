import time
from bot.strategies import STRATEGIES


MAX_TIME_TO_REPLY = 2 * 86400  # 2 days


class PrisonersDilemmaBot:
    def __init__(
        self, strategy="tit_for_tat", game_matrix=[5, 3, 1, 0], moves_to_play=10
    ):
        self.moves_to_play = moves_to_play
        self.game_matrix = game_matrix
        self.active_games = {}
        self.strategy = STRATEGIES.get(strategy, STRATEGIES[list(STRATEGIES.keys())[0]])

    def play(self, user, opponent_move):
        # Get the active game
        game = self.active_games.get(user, None)

        # Check if there is no active game for this user or the user didn't play for a long time
        if not game or time.time() - game["last_time"] > MAX_TIME_TO_REPLY:
            self.active_games[user] = dict(
                start_time=time.time(), last_time=time.time(), moves=[], points=(0, 0)
            )
            return self.active_games[user]

        # Play both moves
        own_move = self.strategy(game["moves"])
        game["moves"].append((own_move, opponent_move))

        # Calculate the outcome and update the total points
        outcomes = self.get_outcomes(own_move, opponent_move)
        game["points"] = (
            game["points"][0] + outcomes[0],
            game["points"][1] + outcomes[1],
        )
        game["last_time"] = time.time()

        # Check if the game is finished and delete
        if len(game["moves"]) == self.moves_to_play:
            del self.active_games[user]

        return game

    def get_outcomes(self, own_move, opponent_move):
        if own_move and opponent_move:
            return (self.game_matrix[1], self.game_matrix[1])
        elif not own_move and opponent_move:
            return (self.game_matrix[0], self.game_matrix[3])
        elif own_move and not opponent_move:
            return (self.game_matrix[3], self.game_matrix[0])
        else:
            return (self.game_matrix[2], self.game_matrix[2])

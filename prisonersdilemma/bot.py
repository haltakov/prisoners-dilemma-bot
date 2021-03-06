"""Module implementing a Prisoner's Dilemma bot"""

import time
import json


class PrisonersDilemmaBot:
    """Bot playing Prisoner's Dilemma with multiple opponents at the same time"""

    def __init__(
        self,
        strategy,
        game_matrix=(5, 3, 1, 0),
        moves_to_play=10,
        timeout=2 * 86400,
    ):
        """Initializes a new Prisoner's Dilemma bot

        :param strategy: function implementing a particular strategy
        :param game_matrix: matrix with game payoffs, defaults to [5, 3, 1, 0]
        :param moves_to_play: number of moves to play with each opponent, defaults to 10
        :param timeout: timeout after which the current game for the opponen will be discarded,
        defaults to 2 days
        """
        self.strategy = strategy
        self.game_matrix = game_matrix
        self.moves_to_play = moves_to_play
        self.timeout = timeout

        self.active_games = {}

    def is_user_playing(self, user):
        """Check if a user is currently playing a game

        :param user: user
        """
        return user in self.active_games

    def play(self, user, opponent_move):
        """Play a single move of the Prisoner's Dilemma game with one opponent

        :param user: name of the opponent
        :param opponent_move: move of the opponent: True for COOPERATE and False for DEFECT
        :return: The current game state for this opponent - a dict containing the start and last
        played time, the moves history and the current scores
        """
        # Get the active game
        game = self.active_games.get(user, None)

        # Check if there is no active game for this user or the user didn't play for a long time
        if not game or time.time() - game["last_time"] > self.timeout:
            self.active_games[user] = dict(
                start_time=time.time(),
                last_time=time.time(),
                moves=[],
                total_points=[0, 0],
                last_points=[0, 0],
            )
            return self.active_games[user]

        # Play both moves
        own_move = self.strategy(game["moves"])
        game["moves"].append([own_move, opponent_move])

        # Calculate the outcome and update the total points
        payoffs = self.get_payoffs(own_move, opponent_move)
        game["last_points"] = payoffs
        game["total_points"] = [
            game["total_points"][0] + payoffs[0],
            game["total_points"][1] + payoffs[1],
        ]
        game["last_time"] = time.time()

        # Check if the game is finished and delete
        if len(game["moves"]) == self.moves_to_play:
            del self.active_games[user]

        return game

    def get_payoffs(self, own_move, opponent_move):
        """Compute the payoffs of a single round

        :param own_move: own move encoded as a boolean
        :param opponent_move: opponent move encoded as a boolean
        :return: A pair containing the payoffs for both users
        """
        if own_move and opponent_move:
            return [self.game_matrix[1], self.game_matrix[1]]
        elif not own_move and opponent_move:
            return [self.game_matrix[0], self.game_matrix[3]]
        elif own_move and not opponent_move:
            return [self.game_matrix[3], self.game_matrix[0]]
        else:
            return [self.game_matrix[2], self.game_matrix[2]]

    def load_active_games(self, filename):
        """Load the active games from a JSON file

        :param filename: path to the file where the games are saved
        """
        with open(filename, "r") as json_file:
            self.active_games = json.load(json_file)

    def save_active_games(self, filename):
        """Save the active games to a JSON file

        :param filename: path to the file where the games will be saved
        """
        with open(filename, "w") as json_file:
            json.dump(self.active_games, json_file)

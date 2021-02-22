import json
import argparse


def parse_args():
    description = (
        """Read the archived games file and sort the games by the final score"""
    )

    parser = argparse.ArgumentParser(description=description)

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

    # Read all games
    with open(args.archive_file) as archive:
        all_games = [json.loads(game_json) for game_json in archive.readlines()]

    # Extract the game score and sort
    game_scores = map(
        lambda game: dict(user=game["user"], score=game["total_points"][1]),
        all_games,
    )
    game_scores = sorted(game_scores, key=lambda game: game["score"], reverse=True)

    # Print the scores
    for game in game_scores:
        print(f"@{game['user']}\t\t{game['score']}")
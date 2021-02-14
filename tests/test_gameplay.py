import time
import pytest
from unittest.mock import patch
from bot.prisoners_dilemma_bot import PrisonersDilemmaBot


def test_new_game():
    bot = PrisonersDilemmaBot()

    expect_game_state(bot.play("test_user_1", True), [], (0, 0))
    expect_game_state(bot.play("test_user_2", True), [], (0, 0))


def expect_game_state(game_state, expected_moves, expected_points):
    assert game_state["moves"] == expected_moves
    assert game_state["points"] == expected_points


def test_short_game_draw():
    bot = PrisonersDilemmaBot(strategy="always_cooperate", moves_to_play=1)

    bot.play("test_user", "@DilemmaBot let's play")
    expect_game_state(bot.play("test_user", True), [(True, True)], (3, 3))


def test_short_game_win():
    bot = PrisonersDilemmaBot(strategy="always_cooperate", moves_to_play=1)

    bot.play("test_user", "@DilemmaBot let's play")
    expect_game_state(bot.play("test_user", False), [(True, False)], (0, 5))


def test_short_game_lose():
    bot = PrisonersDilemmaBot(strategy="always_defect", moves_to_play=1)

    bot.play("test_user", "@DilemmaBot let's play")
    expect_game_state(bot.play("test_user", True), [(False, True)], (5, 0))


def test_long_game():
    bot = PrisonersDilemmaBot(moves_to_play=4)

    bot.play("test_user", "@DilemmaBot let's play")
    expect_game_state(bot.play("test_user", True), [(True, True)], (3, 3))
    expect_game_state(
        bot.play("test_user", False), [(True, True), (True, False)], (3, 8)
    )
    expect_game_state(
        bot.play("test_user", False),
        [(True, True), (True, False), (False, False)],
        (4, 9),
    )
    expect_game_state(
        bot.play("test_user", True),
        [(True, True), (True, False), (False, False), (False, True)],
        (9, 9),
    )


def test_parallel_games():
    bot = PrisonersDilemmaBot(moves_to_play=2)

    bot.play("test_user_1", "@DilemmaBot let's play")
    expect_game_state(bot.play("test_user_1", True), [(True, True)], (3, 3))

    bot.play("test_user_2", "@DilemmaBot let's play")
    expect_game_state(bot.play("test_user_2", False), [(True, False)], (0, 5))

    expect_game_state(
        bot.play("test_user_1", False), [(True, True), (True, False)], (3, 8)
    )

    expect_game_state(
        bot.play("test_user_2", False), [(True, False), (False, False)], (1, 6)
    )


def test_game_timeout():
    bot = PrisonersDilemmaBot(moves_to_play=2)

    bot.play("test_user_1", "@DilemmaBot let's play")
    expect_game_state(bot.play("test_user_1", True), [(True, True)], (3, 3))

    bot.active_games["test_user_1"]["start_time"] -= 200000
    bot.active_games["test_user_1"]["last_time"] -= 200000

    expect_game_state(bot.play("test_user_1", True), [], (0, 0))
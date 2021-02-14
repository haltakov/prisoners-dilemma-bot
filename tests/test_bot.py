"""Tests for the Prisoner's Dilemma bot"""

from prisonersdilemma.bot import PrisonersDilemmaBot
import prisonersdilemma.strategy as strategy


def test_new_game():
    """Test starting a new game"""
    bot = PrisonersDilemmaBot(strategy.play_tit_for_tat)

    expect_game_state(bot.play("test_user_1", True), [], (0, 0))
    expect_game_state(bot.play("test_user_2", True), [], (0, 0))


def expect_game_state(game_state, expected_moves, expected_points):
    """Helper function to compare the given game state to an expected game state

    :param game_state: actual game state
    :param expected_moves: expected moves history
    :param expected_points: expected points
    """
    assert game_state["moves"] == expected_moves
    assert game_state["points"] == expected_points


def test_short_game_draw():
    """Test a short game ending with a draw"""
    bot = PrisonersDilemmaBot(strategy.play_always_cooperate, moves_to_play=1)

    bot.play("test_user", "@DilemmaBot let's play")
    expect_game_state(bot.play("test_user", True), [(True, True)], (3, 3))


def test_short_game_win():
    """Test a short game ending with a win for the opponent"""
    bot = PrisonersDilemmaBot(strategy.play_always_cooperate, moves_to_play=1)

    bot.play("test_user", "@DilemmaBot let's play")
    expect_game_state(bot.play("test_user", False), [(True, False)], (0, 5))


def test_short_game_lose():
    """Test a short game ending with a defeat for the opponent"""
    bot = PrisonersDilemmaBot(strategy.play_always_defect, moves_to_play=1)

    bot.play("test_user", "@DilemmaBot let's play")
    expect_game_state(bot.play("test_user", True), [(False, True)], (5, 0))


def test_long_game():
    """Test a long game featuring all possible move combinations"""
    bot = PrisonersDilemmaBot(strategy.play_tit_for_tat, moves_to_play=4)

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
    """Test 2 games with different opponents being played in parallel"""
    bot = PrisonersDilemmaBot(strategy.play_tit_for_tat, moves_to_play=2)

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
    """Test game timeout"""
    bot = PrisonersDilemmaBot(strategy.play_tit_for_tat, moves_to_play=2)

    bot.play("test_user_1", "@DilemmaBot let's play")
    expect_game_state(bot.play("test_user_1", True), [(True, True)], (3, 3))

    bot.active_games["test_user_1"]["start_time"] -= 200000
    bot.active_games["test_user_1"]["last_time"] -= 200000

    expect_game_state(bot.play("test_user_1", True), [], (0, 0))

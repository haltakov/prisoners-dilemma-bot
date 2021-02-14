import pytest
from bot.prisoners_dilemma_bot import PrisonersDilemmaBot


def test_parse_move():
    bot = PrisonersDilemmaBot()

    assert bot.parse_move("I cooperate now")
    assert bot.parse_move("I cOoPeRAte now")
    assert bot.parse_move("COOPERATE")
    assert bot.parse_move("cooperate")
    assert bot.parse_move("C")
    assert bot.parse_move("c")
    assert bot.parse_move(" c  ")

    assert not bot.parse_move("I defect now")
    assert not bot.parse_move("I dEfEcT now")
    assert not bot.parse_move("DEFECT")
    assert not bot.parse_move("defect")
    assert not bot.parse_move("D")
    assert not bot.parse_move("d")
    assert not bot.parse_move(" d  ")

    with pytest.raises(ValueError):
        bot.parse_move("No correct move")

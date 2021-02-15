"""Tests for the Twitter client"""

import pytest
import prisonersdilemma.twitter_client as twitter_client


def test_parse_move():
    """Test the parsing of the move from a text"""

    assert twitter_client.parse_move("I cooperate now")
    assert twitter_client.parse_move("I cOoPeRAte now")
    assert twitter_client.parse_move("COOPERATE")
    assert twitter_client.parse_move("cooperate")
    assert twitter_client.parse_move("C")
    assert twitter_client.parse_move("c")
    assert twitter_client.parse_move(" c  ")

    assert not twitter_client.parse_move("I defect now")
    assert not twitter_client.parse_move("I dEfEcT now")
    assert not twitter_client.parse_move("DEFECT")
    assert not twitter_client.parse_move("defect")
    assert not twitter_client.parse_move("D")
    assert not twitter_client.parse_move("d")
    assert not twitter_client.parse_move(" d  ")

    with pytest.raises(ValueError):
        twitter_client.parse_move("No correct move")

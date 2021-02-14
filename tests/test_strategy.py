"""Tests for the Prisoners Dilemma strategies"""

import prisonersdilemma.strategy


def test_tit_for_tat():
    """Test the tit for tat strategy"""
    strategy = prisonersdilemma.strategy.play_tit_for_tat

    assert strategy([])
    assert strategy([(True, True)])
    assert strategy([(False, True)])
    assert not strategy([(True, False)])
    assert not strategy([(False, False)])
    assert strategy([(False, False), (False, False), (False, False), (False, True)])


def test_always_defect():
    """Test the always defect strategy"""
    strategy = prisonersdilemma.strategy.play_always_defect

    assert not strategy([])
    assert not strategy([(True, True)])
    assert not strategy([(True, False)])
    assert not strategy([(False, True)])
    assert not strategy([(False, False)])


def test_always_cooperate():
    """Test the always cooperate strategy"""
    strategy = prisonersdilemma.strategy.play_always_cooperate

    assert strategy([])
    assert strategy([(True, True)])
    assert strategy([(True, False)])
    assert strategy([(False, True)])
    assert strategy([(False, False)])

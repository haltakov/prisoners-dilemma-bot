from bot.strategies import STRATEGIES


def test_tit_for_tat():
    strategy = STRATEGIES["tit_for_tat"]

    assert strategy([])
    assert strategy([(True, True)])
    assert strategy([(False, True)])
    assert not strategy([(True, False)])
    assert not strategy([(False, False)])
    assert strategy([(False, False), (False, False), (False, False), (False, True)])


def test_always_defect():
    strategy = STRATEGIES["always_defect"]

    assert not strategy([])
    assert not strategy([(True, True)])
    assert not strategy([(True, False)])
    assert not strategy([(False, True)])
    assert not strategy([(False, False)])


def test_always_cooperate():
    strategy = STRATEGIES["always_cooperate"]

    assert strategy([])
    assert strategy([(True, True)])
    assert strategy([(True, False)])
    assert strategy([(False, True)])
    assert strategy([(False, False)])

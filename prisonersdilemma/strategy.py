"""Module defining different Prisoner's Dilemma strategy functions"""


def play_tit_for_tat(moves):
    """Tit For Tat strategy

    This strategy starts with C and after that always repeats the opponent's last move

    :param moves: list of the moves history
    :return: new move chosen by the strategy
    """
    if len(moves) == 0:
        return True
    else:
        return moves[-1][1]


def play_always_defect(_):
    """Always defect strategy

    This strategy always plays D

    :param moves: list of the moves history
    :return: new move chosen by the strategy
    """
    return False


def play_always_cooperate(_):
    """Always cooperate strategy

    This strategy always plays C

    :param moves: list of the moves history
    :return: new move chosen by the strategy
    """
    return True

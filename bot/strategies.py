def play_tit_for_tat(moves):
    if len(moves) == 0:
        return True
    else:
        return moves[-1][1]


def play_always_defect(_):
    return False


def play_always_cooperate(_):
    return True


STRATEGIES = dict(
    tit_for_tat=play_tit_for_tat,
    always_defect=play_always_defect,
    always_cooperate=play_always_cooperate,
)

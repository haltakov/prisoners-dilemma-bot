from bot.prisoners_dilemma_bot import PrisonersDilemmaBot, BOT_REPLIES


def test_new_game():
    bot = PrisonersDilemmaBot()

    assert bot.play("test_user", "@DilemmaBot let's play") == BOT_REPLIES["rules"]
    assert bot.play("test_user_2", "@DilemmaBot let's play") == BOT_REPLIES["rules"]


def test_invalid_move():
    bot = PrisonersDilemmaBot()

    bot.play("test_user", "@DilemmaBot let's play")
    assert bot.play("test_user", "No valid move") == BOT_REPLIES["invalid_move"]


def test_short_game_draw():
    bot = PrisonersDilemmaBot(strategy="always_cooperate", moves_to_play=1)

    bot.play("test_user", "@DilemmaBot let's play")
    assert bot.play("test_user", "C") == BOT_REPLIES["game_update"] % (
        1,
        1,
        "C",
        "C",
        3,
        3,
        3,
        3,
        BOT_REPLIES["result_draw"],
    )


def test_short_game_win():
    bot = PrisonersDilemmaBot(strategy="always_cooperate", moves_to_play=1)

    bot.play("test_user", "@DilemmaBot let's play")
    assert bot.play("test_user", "D") == BOT_REPLIES["game_update"] % (
        1,
        1,
        "D",
        "C",
        5,
        0,
        5,
        0,
        BOT_REPLIES["result_win"],
    )


def test_short_game_lose():
    bot = PrisonersDilemmaBot(strategy="always_defect", moves_to_play=1)

    bot.play("test_user", "@DilemmaBot let's play")
    assert bot.play("test_user", "C") == BOT_REPLIES["game_update"] % (
        1,
        1,
        "C",
        "D",
        0,
        5,
        0,
        5,
        BOT_REPLIES["result_lose"],
    )


def test_long_game():
    bot = PrisonersDilemmaBot(moves_to_play=4)

    bot.play("test_user", "@DilemmaBot let's play")

    assert bot.play("test_user", "C") == BOT_REPLIES["game_update"] % (
        1,
        4,
        "C",
        "C",
        3,
        3,
        3,
        3,
        "",
    )

    assert bot.play("test_user", "D") == BOT_REPLIES["game_update"] % (
        2,
        4,
        "D",
        "C",
        5,
        0,
        8,
        3,
        "",
    )

    assert bot.play("test_user", "D") == BOT_REPLIES["game_update"] % (
        3,
        4,
        "D",
        "D",
        1,
        1,
        9,
        4,
        "",
    )

    assert bot.play("test_user", "C") == BOT_REPLIES["game_update"] % (
        4,
        4,
        "C",
        "D",
        0,
        5,
        9,
        9,
        BOT_REPLIES["result_draw"],
    )

from bot.prisoners_dilemma_bot import PrisonersDilemmaBot, BOT_REPLIES


def test_new_game():
    bot = PrisonersDilemmaBot()

    assert bot.play("test_user", "@DilemmaBot let's play") == BOT_REPLIES["rules"]
    assert bot.play("test_user_2", "@DilemmaBot let's play") == BOT_REPLIES["rules"]


def test_invalid_move():
    bot = PrisonersDilemmaBot()

    bot.play("test_user", "@DilemmaBot let's play")
    assert bot.play("test_user", "No valid move") == BOT_REPLIES["invalid_move"]
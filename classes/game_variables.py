class ExitScript(Exception):
    pass

class GameConstants():
    GAME_HEIGHT = 50
    GAME_WIDTH = 120

class GameVariables():
    paused = False
    closing_game = False
    skip_next_input = False
    wins=0
    loses=0
    min_word_len = 1
    max_word_len = 31
    playtime = False
    guessing = ""
    failed_letters = ""
    failed_words = ""
    lives = 8
    good_word = ""
    good_list = ""
    good_list = []
    unknown_list = []
            
class GameWindows():
    pass
    # main_win
    # pause_menu
    # guess_word
    # flower
    # logs
    # player_guess
    # incorrect
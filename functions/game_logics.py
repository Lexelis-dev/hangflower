import json
import random
import curses

from .helpers import ask_key, refresh_main_win
from classes import GameConstants as GCon
from classes import GameVariables as GVar
from classes import GameWindows as GWin

file = open('words_dictionary.json')
data = json.load(file)
words = list(data.keys())
    
def game_initialisation():
    GVar.playtime = True
        
def randword():
    while True:
        chosen_word = random.choice(words)
        if GVar.min_word_len <= len(chosen_word) <= GVar.max_word_len:
            return chosen_word
        
def guess_change(key):
    if ((key in range(97,123) or key in range(65, 91))
        and len(GVar.guessing) < GVar.max_word_len):
        
        GVar.guessing += chr(key).lower()
    elif key == 8: # BACKSPACE
        GVar.guessing = GVar.guessing[:-1]
    elif key == 10: # ENTER
        plr_choice = GVar.guessing
        GVar.guessing = ""
        return plr_choice
    
def guess_check(plr_choice):
    if len(plr_choice) == 1:
        if plr_choice in GVar.good_word:
            find_letter(plr_choice)
        else:
            fail(plr_choice)
    else:
        if plr_choice != GVar.good_word:
            fail(plr_choice)
    
def find_letter(plr_choice):
    for index, letter in enumerate(GVar.good_list):
        if letter == plr_choice:
            GVar.unknown_list[index] = plr_choice
            
def fail(plr_choice):
    GVar.lives -= 1
    if len(plr_choice) == 1:
        if plr_choice not in GVar.failed_letters:
            GVar.failed_letters += plr_choice
    else:
        GVar.failed_words += plr_choice +"  "

def win():
    GVar.wins += 1
    pass

def lose():
    GVar.loses += 1
    # TODO show the correct word
    # TODO concecutive wins
    pass

def reset_game():
    GVar.lives = 8
    GVar.good_word = randword()
    GVar.good_list = [x for x in GVar.good_word]
    GVar.unknown_list = ["_" for x in GVar.good_word]
    GVar.failed_letters = ""
    GVar.failed_words = ""
    print(GVar.good_word)
        
def playtime():
    reset_game()
    
    while True:
        playtime_refresh()
        
        key = ask_key()
        if (key != -1) and (key != curses.KEY_RESIZE):
            plr_choice = guess_change(key)
        
        if plr_choice :
            guess_check(plr_choice)
            playtime_refresh()
            
        playtime_refresh()
        
        if GVar.lives == 0:
            lose()
            break
        elif GVar.good_word == plr_choice or GVar.good_list == GVar.unknown_list :
            win()
            break
            
flower = """
 _,-._\n
/ \_/ \ \n
>-(_)-<\n
\_/ \_/\n
  `-'\n
"""

def playtime_screen():
    GWin.incorrect.border()
    GWin.player_guess.clear()
    GWin.player_guess.border()
    GWin.guess_word.border()
    GWin.flower.border()
    GWin.logs.border()
    
    GWin.flower.addstr(3,11,"_,-._")
    GWin.flower.addstr(4,10,"/ \\_/ \\")
    GWin.flower.addstr(5,10,">-(_)-<")
    GWin.flower.addstr(6,10,"\_/ \_/")
    GWin.flower.addstr(7,12,"`-'")
    
    GWin.player_guess.addstr(5,
                             GCon.GAME_WIDTH//2 - len(GVar.guessing)//2,
                             GVar.guessing)
    
def playtime_refresh():
    playtime_screen()
    refresh_main_win()
    printed_word = " ".join(GVar.unknown_list)
    log = f"Wins : {GVar.wins}   Loses : {GVar.loses}"
    GWin.guess_word.addstr(20 // 2,
                         (80 - len(printed_word)) // 2,
                         printed_word)
    GWin.guess_word.addstr(1, 2, f"Remaining lives : {GVar.lives}")
    GWin.incorrect.addstr(2, 2, GVar.failed_letters)
    GWin.incorrect.addstr(5, 2, GVar.failed_words)
    GWin.logs.addstr(2,
              GCon.GAME_WIDTH//2 - len(log)//2,
              log)
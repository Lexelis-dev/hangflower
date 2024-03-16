import curses

from classes import ExitScript
from classes import GameConstants as GCon
from classes import GameVariables as GVar
from classes import GameWindows as GWin
from functions import (randword, ask_key, exit_check, show_pause_menu,
                       skip_next_input, game_initialisation, playtime)

        
def main(stdscr):
    GWin.stdscr = stdscr
    # Initialisation
    curses.curs_set(0)  # Hide the cursor
    
    curses.resize_term(GCon.GAME_HEIGHT+5, GCon.GAME_WIDTH+14)
    screen_height, screen_width = stdscr.getmaxyx()
    
    main_win = curses.newwin(GCon.GAME_HEIGHT, GCon.GAME_WIDTH, 0, 0)
    pause_menu = curses.newwin(GCon.GAME_HEIGHT//2,
                               GCon.GAME_WIDTH, GCon.GAME_HEIGHT//4, 0)
   
    guess_word = main_win.subwin(20, 80, 5, 0)
    flower = main_win.subwin(20, 40, 5, 80)
    logs = main_win.subwin(5, GCon.GAME_WIDTH, 0, 0)
    player_guess = main_win.subwin(11, GCon.GAME_WIDTH, 24, 0)
    incorrect = main_win.subwin(16, GCon.GAME_WIDTH, 34, 0)
    
    GWin.guess_word = guess_word
    GWin.flower = flower
    GWin.logs = logs
    GWin.player_guess = player_guess
    GWin.incorrect = incorrect
    
    GWin.main_win = main_win
    GWin.pause_menu = pause_menu
    
    GWin.pause_menu.mvwin(screen_height//2-GCon.GAME_HEIGHT//4,
                          screen_width//2-GCon.GAME_WIDTH//2)
    GWin.main_win.mvwin(screen_height//2-GCon.GAME_HEIGHT//2,
                        screen_width//2-GCon.GAME_WIDTH//2)
    
    stdscr.nodelay(True)
    
    def inner_main():
        game_initialisation()
        while True:
            GWin.main_win.clear()
            GWin.main_win.border()
        
            GWin.main_win.refresh()
            show_pause_menu() 
            
            if GVar.playtime == True:
                playtime()
            
            if not GVar.skip_next_input:
                key = ask_key()
            
            else:
                skip_next_input(False)
            
    try:
        inner_main()
    except ExitScript:
        pass
    
# Initialise if the script is executed
if __name__ == "__main__":
    curses.wrapper(main)
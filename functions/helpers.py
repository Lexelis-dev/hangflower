import curses

from classes import ExitScript
from classes import GameConstants as GCon
from classes import GameVariables as GVar
from classes import GameWindows as GWin

def ask_key(checking_exit = True):
    while True:
        try :
            key = GWin.stdscr.getch()
            
        except curses.error:
            pass
        
        if (key != -1) and (key != curses.KEY_RESIZE):
            if key == 27:
                if GVar.paused == True:
                    return "leave"
                else:
                    GVar.paused = True
                    return ""
            else:
                return key
        
        elif key !=-1 and key == curses.KEY_RESIZE:
            resize_screen(GWin.main_win, GCon.GAME_HEIGHT, GCon.GAME_WIDTH)
            if GVar.paused == True:
                resize_screen(GWin.pause_menu, GCon.GAME_HEIGHT//2, GCon.GAME_WIDTH)
        
        if checking_exit:
            exit_check(key)
            
# If the user tries to modify the terminal size
def resize_screen(window, win_height, win_width): # TODO get rid of argument, have windows resize with the correct size
    screen_height, screen_width = GWin.stdscr.getmaxyx()
    
    if screen_height > win_height+5 or screen_width > win_width+14:
        window.mvwin(screen_height//2 - win_height//2,
                     screen_width//2 - win_width//2)
    
    else:
        curses.resize_term(win_height+5, win_width+14)
        screen_height, screen_width = GWin.stdscr.getmaxyx()
        try:
            window.mvwin(screen_height//2 - win_height//2,
                         screen_width//2 - win_width//2)
        except curses.error:
            pass
    curses.curs_set(0)
    window.refresh()
        
def refresh_main_win():
    resize_screen(GWin.main_win, GCon.GAME_HEIGHT, GCon.GAME_WIDTH)
    
def exit_check(key):
    # Key is Escape
    if GVar.paused == True:
        while True:
            show_pause_menu()
            GWin.main_win.refresh()
            key = ask_key(False)
            
            if key == "leave":
                raise ExitScript
            
            # Key is either Enter or Space
            elif key in (32,10):
                GVar.paused = False 
                GWin.pause_menu.clear()
                GWin.pause_menu.refresh()
                refresh_main_win()
                break
            
def show_pause_menu():
    if GVar.paused == True:
        resize_screen(GWin.pause_menu, GCon.GAME_HEIGHT//2, GCon.GAME_WIDTH)
        GWin.pause_menu.border()
        message = "Press escape again to leave"
        GWin.pause_menu.addstr(GCon.GAME_HEIGHT//4,
                            GCon.GAME_WIDTH//2-len(message)//2,
                            message) # TODO function to print middle
        
        GWin.pause_menu.refresh()
        GWin.main_win.refresh()
    else:
        GWin.pause_menu.clear()
        
def skip_next_input(state = True):
    GVar.skip_next_input = state
    

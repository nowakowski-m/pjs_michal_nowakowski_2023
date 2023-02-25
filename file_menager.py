import system_functions as sf
import run_functions as rf
import keyboard
import curses

curr_win_res = [rf.win_w(), rf.win_h()]
highlighted_item = 1

while True:

    rf.check_win_res(curr_win_res, highlighted_item)

    if (keyboard.is_pressed('up') or keyboard.is_pressed('down')): 
        if (keyboard.is_pressed('up')) and highlighted_item in range (2, (len(sf.list_items()) + 1)):
            highlighted_item -= 1
        if (keyboard.is_pressed('down')) and highlighted_item in range (0, len(sf.list_items())):
            highlighted_item += 1

        rf.render_list(highlighted_item)
    
    curr_win_res = [rf.win_w(), rf.win_h()]

    # curses.napms(1)

    if (keyboard.is_pressed('esc')):
        rf.end_functions()
        break
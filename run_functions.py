import system_functions as sf
import keyboard
import curses
import os

def fm_win():
    return curses.initscr()

def win_w():
    return os.get_terminal_size().lines

def win_h():
    return os.get_terminal_size().columns

def render_list(highlighted_item):

    x_pos = 20
    y_pos = round ((win_w() - len(sf.list_items())) / 2)
    y_plus = 0

    for item_index in sf.list_items():
        
        item = f'{sf.list_items()[item_index]}'
        
        if item_index == 1:
            curr_x_pos = x_pos
        elif item_index != 1:
            curr_x_pos = x_pos + 5

        if item_index == highlighted_item:
            fm_win().addstr((y_pos + y_plus), curr_x_pos, item, color()[1])

        elif item_index != highlighted_item:
            fm_win().addstr((y_pos + y_plus), curr_x_pos, item, color()[2])

        # if item_index == highlighted_item:
        #     item = f'{sf.list_items()[item_index]}'
        #     fm_win().addstr((y_pos + y_plus), x_pos + 5, item, color()[2])
        # else:
        #     item = f'{sf.list_items()[item_index]}'
        #     fm_win().addstr((y_pos + y_plus), x_pos + 5, item, color()[1])
        y_plus += 1

    return fm_win().refresh()

def check_win_res(curr_win_res, highlighted_item):

    new_win_w = win_w()
    new_win_h = win_h()

    if (new_win_w != curr_win_res[0]) or (new_win_h != curr_win_res[1]):
        fm_win().clear()
        render_list(highlighted_item)

def color():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    color_0 = "" # empty for index compatibillity
    color_1 = curses.color_pair(1)
    color_2 = curses.color_pair(2)

    return color_0, color_1, color_2

def end_functions():
    curses.endwin()
    keyboard.press_and_release('ctrl+c')
    os.system('clear')
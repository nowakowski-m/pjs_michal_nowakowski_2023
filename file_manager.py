# https://github.com/nowakowski-m/pjs_michal_nowakowski_2023
# This is main file, execute it to run app.

import system_functions as sf #temporary app module with whole functionality
import curses #tool used for user interface

### Variables and configs section ###
use_cfg = sf.load_settings()
show_hidden_items, useless_thing = use_cfg[0]
highlighted_item, path = use_cfg[1]
#####################################

stdscr = curses.initscr()
menu_shadow = sf.screen_elements(stdscr)[0]
menu = sf.screen_elements(stdscr)[1]

sf.start_things(stdscr, menu_shadow, menu)

while True:
    
    height, width = stdscr.getmaxyx()

    menu.addstr(((menu.getmaxyx()[0]) - 2), 2, "ESC - Exit", curses.color_pair(4)) #just testing sth
    
    path = sf.render_things(menu, show_hidden_items, highlighted_item)
    key = menu.getch()
    highlighted_item += (sf.sterring(key, path, show_hidden_items, highlighted_item) if key else 0)

    if key == 27:
        sf.close_functions(menu)
        break

    if curses.is_term_resized(height, width):
        sf.change_size(stdscr, menu_shadow, menu)
# https://github.com/nowakowski-m/pjs_michal_nowakowski_2023
# This is main file, execute it to run app.

import system_functions as sf #temporary app module with whole functionality
import curses #tool used for user interface

####### Variables and configs section #######
use_cfg = sf.load_settings()
show_hidden_items, useless_thing = use_cfg[0]
highlighted_item, path, current_page = use_cfg[1]

stdscr = curses.initscr()
menu_shadow = sf.screen_elements(stdscr)[0]
menu = sf.screen_elements(stdscr)[1]
max_list_len = sf.screen_elements(stdscr)[2]

sf.start_things(stdscr, menu_shadow, menu)
#############################################

while True:
    
    height, width = stdscr.getmaxyx()

    list_len = (len(sf.list_items(show_hidden_items, max_list_len)) - 1)
    items_pages = (((list_len // max_list_len) + 1) if list_len > max_list_len else 1)
    path = sf.render_things(menu, show_hidden_items, highlighted_item, max_list_len, items_pages, current_page)
    key = menu.getch()
    highlighted_item += (sf.sterring(key, path, highlighted_item, current_page, items_pages, list_len, max_list_len) if key else 0)
    current_page += (sf.change_page(key, current_page, items_pages, path))
   
    if key == 27:
        sf.close_functions(menu)
        break

    if curses.is_term_resized(height, width):
        sf.change_size(stdscr, menu_shadow, menu)
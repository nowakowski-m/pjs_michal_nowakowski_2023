# https://github.com/nowakowski-m/pjs_michal_nowakowski_2023
# This is main file, execute it to run app.

import system_functions as sf #temporary app module with whole functionality
import curses #tool used for user interface

############### Variables and configs section ###############
use_cfg = sf.load_settings()
stdscr = curses.initscr()
show_hidden_items, useless_thing = use_cfg[0]
highlighted_item, path, current_page, items_pages = use_cfg[1]
menu_shadow, menu, max_list_len = sf.screen_elements()
sf.start_things(stdscr, menu_shadow, menu)
#############################################################

while True:
    
    height, width = stdscr.getmaxyx()

    first_index = (max_list_len + 1) * (current_page - 1)
    list_len = (len(sf.list_items(show_hidden_items, items_pages, max_list_len)) - 1)
    items_pages = (((list_len // max_list_len) + 1) if list_len > max_list_len else 1)
    last_index = first_index + max_list_len
    
    path = sf.render_things(menu, show_hidden_items, highlighted_item, max_list_len, items_pages, current_page, first_index, last_index)
    key = menu.getch()
    highlighted_item += (sf.sterring(key, menu, path, highlighted_item, last_index, current_page, items_pages, list_len, max_list_len) if key else sf.check_highlight(highlighted_item, first_index, last_index))
    current_page += (sf.change_page(key, highlighted_item, current_page, items_pages, first_index, last_index, path))
   
    if key == 27:
        sf.close_functions(menu)
        break

    if curses.is_term_resized(height, width):
        sf.change_size(stdscr, menu_shadow, menu)
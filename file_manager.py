# https://github.com/nowakowski-m/pjs_michal_nowakowski_2023
# This is main file, execute it to run app.

import system_functions as sf #temporary app module with whole functionality
import curses #tool used for user interface
import os #for system commands

############### Variables and configs section ###############
use_cfg = sf.load_settings()
stdscr = curses.initscr()
show_hidden_items, useless_thing = use_cfg[0]
highlighted_item, path, last_path, copy_path, current_page, items_pages, delete_warning, preview_file = use_cfg[1]
menu_shadow, menu, lower_bar, max_list_len, margin = sf.screen_elements()
sf.start_things(stdscr, menu_shadow, menu, lower_bar)
#############################################################

preview_line = 0
preview_len = 0

while True:
    
    height, width = stdscr.getmaxyx()
    
    max_name_len = int(width) - (7 * margin)
    first_index = (max_list_len + 1) * (current_page - 1)
    list_len = (len(sf.list_items(show_hidden_items, items_pages, max_list_len)) - 1)
    items_pages = (((list_len // (max_list_len + 1)) + (0 if list_len % max_list_len == 0 else 1)) if list_len > max_list_len else 1)
    last_index = first_index + max_list_len
    max_list_len = menu.getmaxyx()[0] - 2

    render = sf.render_things(menu, preview_file, preview_line, lower_bar, max_name_len, show_hidden_items, highlighted_item, max_list_len, items_pages, current_page, first_index, last_index)

    path = render[0] if not preview_file else ""
    
    key = menu.getch()
    preview_opt = sf.preview_steering(key, preview_file, preview_line, preview_len, max_list_len)
    preview_file = True if (key == 80 and not preview_file and not os.path.isdir(path) and sf.is_readable(path)) else (preview_opt[1])
    preview_len = render[1] if preview_file else 0
    preview_line += preview_opt[0]

    if not preview_file:
        highlighted_item += (sf.steering(key, lower_bar, path, last_path, highlighted_item, last_index, current_page, items_pages, list_len, max_list_len, delete_warning) if key else sf.check_highlight(highlighted_item, first_index, last_index))
        current_page += (sf.change_page(key, highlighted_item, current_page, items_pages, first_index, last_index, path))
        deleting_item = sf.delete_item(lower_bar, path, last_path, delete_warning) if key == 68 else [0, False, ""]
        delete_warning = (deleting_item)[1] if key == 68 else delete_warning
        last_path = (deleting_item)[2] if key == 68 else last_path
    
        if key == 67 or key == 77 or key == 86:
            copy_path = (sf.copy_paste_move(path, copy_path, key))
        
        if key == 27:
            sf.close_functions(menu)
            break

    if curses.is_term_resized(height, width):
        sf.change_size(stdscr, menu_shadow, menu, lower_bar)
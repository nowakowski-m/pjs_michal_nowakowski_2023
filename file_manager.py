# https://github.com/nowakowski-m/pjs_michal_nowakowski_2023
# This is main file, execute it to run app.

import system_functions as sf #temporary app module with whole functionality
import curses #tool used for user interface

### Some global variables needed ###
highlighted_item = 0
margin = 4
path = ""
####################################

stdscr = curses.initscr()
height, width = stdscr.getmaxyx()
menu_shadow = curses.newwin((height - (2 * margin) - 1), (width - (4 * margin)) - 2, (margin + 1), ((2 * margin) + 2))
menu = curses.newwin((height - (2 * margin) - 1), (width - (4 * margin) - 2), margin, (2 * margin))

sf.start_things(stdscr, menu_shadow, menu)

while True:
    
    menu.addstr(((menu.getmaxyx()[0]) - 2), 2, "ESC - Exit", curses.color_pair(4)) #just testing sth
    path = sf.render_things(menu, highlighted_item)
    key = menu.getch()
    highlighted_item += (sf.sterring(key, path, highlighted_item) if key else 0)

    if key == 27:
        sf.close_functions(menu)
        break
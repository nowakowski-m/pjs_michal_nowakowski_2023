import system_functions as sf
import curses
import os

def main(stdscr):
    highlighted_item = 1

    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    stdscr.bkgd(curses.color_pair(1))

    height, width = stdscr.getmaxyx()

    title = "LAHIM"
    stdscr.box()
    stdscr.addstr(0, max(0, (width - len(title)) // 2), f' {title} ')

    x = max(0, 20)
    y = max(0, (height - 1) // 2)
    
    for item_index in sf.list_items():
        if item_index == highlighted_item:
            stdscr.addstr(y, x, sf.list_items()[item_index], curses.color_pair(2))
        else:
            stdscr.addstr(y, x, sf.list_items()[item_index])
        y += 1

    stdscr.refresh()

    while True:

        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            highlighted_item += 1
            x = max(0, 20)
            y = max(0, (height - 1) // 2)

            for item_index in sf.list_items():
                if item_index == highlighted_item:
                    stdscr.addstr(y - 1, x, sf.list_items()[int(item_index) - 1])
                    stdscr.addstr(y, x, sf.list_items()[item_index], curses.color_pair(2))
                y += 1

        elif key == curses.KEY_UP:
            highlighted_item -= 1
            x = max(0, 20)
            y = max(0, (height - 1) // 2)

            for item_index in sf.list_items():
                if item_index == highlighted_item:
                    stdscr.addstr(y, x, sf.list_items()[item_index], curses.color_pair(2))
                    stdscr.addstr(y + 1, x, sf.list_items()[int(item_index) + 1])
                y += 1

        elif key == 10 and ("°" in (sf.list_items()[highlighted_item]) or "𝔻" in (sf.list_items()[highlighted_item])):

            if "°" in (sf.list_items()[highlighted_item]):
                os.chdir("..")

            else:                
                path = (sf.list_items()[highlighted_item])[3::]
                os.chdir(path)

            highlighted_item = 1
            x = max(0, 20)
            y = max(0, (height - 1) // 2)

            stdscr.clear()

            for item_index in sf.list_items():
                if item_index == highlighted_item:
                    stdscr.addstr(y, x, sf.list_items()[item_index], curses.color_pair(2))
                else:
                    stdscr.addstr(y, x, sf.list_items()[item_index])
                y += 1

            stdscr.box()
            stdscr.addstr(0, max(0, (width - len(title)) // 2), f' {title} ')

            stdscr.refresh()

        highlighted_item = max(1, min(len(sf.list_items()), highlighted_item))
        curses.napms(30)

if __name__ == '__main__':
    curses.wrapper(main)
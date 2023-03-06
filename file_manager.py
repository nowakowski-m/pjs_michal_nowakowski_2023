import system_functions as sf
import run_functions as rf
import curses

def main(stdscr):
    height, width = stdscr.getmaxyx()
    highlighted_item = 1
    max_highlight = len(sf.list_items())
    pos = 0
    title = "LAHIM"
    curses.KEY_ENTER = 10
    rf.window_config(stdscr)
    rf.add_box(stdscr, title, width)
    for items in rf.render_new_dir(height, width, highlighted_item):
        stdscr.addstr(*items)

    while True:

        key = stdscr.getch()
        curses.napms(30)

        if key == curses.KEY_DOWN and (highlighted_item < max_highlight):
            pos = 1
            for items in rf.update_curr_dir(pos, highlighted_item, height, width):
                stdscr.addstr(*items)
            highlighted_item += pos

        elif key == curses.KEY_UP and (highlighted_item > 1):
            pos = (-1)
            for items in rf.update_curr_dir(pos, highlighted_item, height, width):
                stdscr.addstr(*items)            
            highlighted_item += pos

        elif key == curses.KEY_ENTER:
            if '𝔻' in sf.list_items()[highlighted_item] or '°' in sf.list_items()[highlighted_item]:
                rf.change_dir(highlighted_item)
                stdscr.clear()
                rf.add_box(stdscr, title, width)
                highlighted_item = 1
                max_highlight = len(sf.list_items())
                for items in rf.render_new_dir(height, width, highlighted_item):
                    stdscr.addstr(*items)
                stdscr.refresh()

        highlighted_item = max(1, min(len(sf.list_items()), highlighted_item))

if __name__ == '__main__':
    curses.wrapper(main)
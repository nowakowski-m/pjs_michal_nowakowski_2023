import system_functions as sf
import curses

def window_config(stdscr):
    curses.curs_set(0)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    stdscr.bkgd(curses.color_pair(1))

def add_box(stdscr, title, width):
    stdscr.box()
    stdscr.addstr(0, max(0, (width - len(title)) // 2), f' {title} ')

# change x and y for filling the screen
def check_space(height, width):
    x = max(0, 20)
    y = max(0, (height - 1) // 2)

    return x, y

def render_new_dir(height, width, highlighted_item):
    xy = check_space(height, width)
    things_to_add = []
    y = xy[1]

    for item_index in sf.list_items():
        if item_index == highlighted_item:
            things_to_add.append([y, xy[0], sf.list_items()[item_index], curses.color_pair(2)])
        else:
            things_to_add.append([y, xy[0], sf.list_items()[item_index]])
        y += 1

    return things_to_add

def update_curr_dir(pos, highlighted_item, height, width):
    xy = check_space(height, width)
    things_to_update = []
    y = xy[1]

    for item_index in sf.list_items():
        if item_index == highlighted_item:
            things_to_update.append([y, xy[0], sf.list_items()[item_index]])
            things_to_update.append([y + pos, xy[0], sf.list_items()[int(item_index) + pos], curses.color_pair(2)])
            break
        y += 1

    return things_to_update

def change_dir(highlighted_item):
    curr_item = (sf.list_items()[highlighted_item])
    if ('°' in curr_item):
        sf.prev_dir()
    else:                
        path = curr_item[3::]
        sf.marked_div(path)
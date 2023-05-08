import curses   #for TUI, graphical terminal interface
import yaml     #support for yaml settings file
import os       #for manipulating system status, controling and reading files/dirs
from shlex import quote #for well formated paths in copy-move-paste function

##### OPENING FUNCTIONS #####

def screen_elements(): #initializing new windows and returns it
    
    margin, height, width, lines, cols = get_sizes()
    menu_shadow = curses.newwin(lines, cols, (margin + 1), ((2 * margin) + 2))
    menu = curses.newwin((lines - 3), cols, margin, (2 * margin))
    lower_bar = curses.newwin(lines, cols, margin, (2 * margin))
    max_list_len = menu.getmaxyx()[0] - 2

    return menu_shadow, menu, lower_bar, max_list_len, margin

def load_settings() -> list: #loads settings file and returns it values as lists
    
    with open('/home/nowakowski-m/Programowanie/Semestr 2/PJS2023/settings.yaml') as f:
        config = yaml.safe_load(f)

    user_settings = [x for x in config["user_settings"].values()]
    global_variables = [y for y in config["global_variables"].values()]

    return user_settings, global_variables

def start_things(stdscr, menu_shadow, menu, lower_bar): #just inits needed things for curses library usage in this app
    
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)

    curses.start_color()
    curses.init_color(1, 169, 184, 427) #blue window background
    curses.init_color(2, 75, 976, 769) #cyan app shadow
    curses.init_color(3, 918, 75, 569) #pink app background
    curses.init_color(4, 0, 0, 0) #black hotkeys tips background
    curses.init_color(5, 75, 976, 769) #cyan app shadow
    curses.init_color(254, 918, 75, 569) #pink bg for no item highlight
    curses.init_color(255, 75, 976, 769) #cyan item highlight
    curses.init_pair(1, curses.COLOR_BLACK, 1)
    curses.init_pair(2, curses.COLOR_BLACK, 2)
    curses.init_pair(3, curses.COLOR_BLACK, 3)
    curses.init_pair(4, curses.COLOR_WHITE, 4)
    curses.init_pair(5, 5, 4)
    curses.init_pair(254, curses.COLOR_BLACK, 254)
    curses.init_pair(255, curses.COLOR_BLACK, 255)

    stdscr.bkgd(curses.color_pair(1))
    stdscr.refresh()
    menu_shadow.bkgd(curses.color_pair(2))
    menu_shadow.refresh()
    menu.bkgd(curses.color_pair(3))
    menu.keypad(True)
    menu.refresh()
    lower_bar.bkgd(curses.color_pair(3))
    lower_bar.refresh()

##### WINDOWS PARAMTERES #####

def get_sizes() -> int: #function create usefull sizes for app, like windows sizes
    
    margin = 4
    height, width = os.popen('stty size', 'r').read().split()
    lines = (int(height) - (2 * margin) - 1)
    cols = (int(width) - (4 * margin) - 2)

    return margin, height, width, lines, cols

def change_size(stdscr, menu_shadow, menu, lower_bar): #resizing windows, when terminal size changed
    
    margin, height, width, lines, cols = get_sizes()
    stdscr.resize(int(height), int(width))
    menu_shadow.resize(lines, cols)
    menu.resize((lines - 3), cols)
    lower_bar.resize(lines, cols)
    stdscr.refresh()
    menu_shadow.refresh()
    menu.refresh()
    lower_bar.refresh()

##### FILES SUPPORT #####

def list_items(show_hidden_items, items_pages, max_list_len) -> list: #checking for items in current dir and prepares list for app needs

    match show_hidden_items:
        case True:
            list_to_get = [f for f in os.listdir()]
        case False:
            list_to_get = [f for f in os.listdir() if not f.startswith('.')]

    higher_dirs = (len(os.getcwd().split("/"))) - 1

    items_list = [] if (len(list_to_get) + items_pages) > max_list_len else [f'° No higher dirs.' if os.getcwd() == "/" else f'° Go back. ({higher_dirs})']

    items_list.extend(f'𝔻 {name}' if os.path.isdir(name) else f'𝔽 {name}' for name in list_to_get)
    
    if (len(list_to_get) + items_pages) > max_list_len:
        for x in range(0, (len(list_to_get) + items_pages), (max_list_len + 1)):
            items_list.insert(x, (f'° No higher dirs.' if os.getcwd() == "/" else f'° Go back. ({higher_dirs})'))
            
    return items_list

def change_dir(lower_bar, path, highlighted_item) -> int: #function changing directory and returning position
    
    try:
        os.chdir(path)
        return (0 - highlighted_item)
    except PermissionError:
        lower_bar.addstr(((lower_bar.getmaxyx()[0]) - 2), 3, "No permissions.", curses.color_pair(4))
        return 0

##### MENU AND IT'S STEERING #####

def render_things(menu, list_len, preview_file, preview_line, lower_bar, max_name_len, show_hidden_items, highlighted_item, max_list_len, items_pages, current_page, first_index, last_index) -> str: #rendering current app status on screen

    menu.clear()
    path = ""

    for index, item in enumerate(list_items(show_hidden_items, items_pages, max_list_len)):
        if index == highlighted_item:
            curr_color = curses.color_pair(255)

            if "𝔻" in item:
                path = item.split("𝔻")[1][1::]
            elif "𝔽" in item:
                path = item.split("𝔽")[1][1::]
            elif "°" in item:
                path = ".."

        else:
            curr_color = curses.color_pair(254)

        y_pos = index - ((max_list_len + 1) * (current_page - 1))

        new_item = item[0:(max_name_len-3)] + "..." if len(item) > max_name_len else item

        if index == first_index and (index <= last_index and index >= first_index):
            menu.addstr((y_pos + 1), 3, new_item, curr_color | curses.A_BOLD)

        elif index != first_index and (index <= last_index and index >= first_index):
            menu.addstr((y_pos + 1), 5, new_item, curr_color)

    pages_string = f"Page: {current_page}/{items_pages}"
    lower_bar.addstr(((lower_bar.getmaxyx()[0]) - 2), (lower_bar.getmaxyx()[1] - len(pages_string) - 2), f"{pages_string}", curses.color_pair(4))
    # lower_bar.addstr((lower_bar.getmaxyx()[0] - 2), 2, f"first: {first_index} last: {last_index}", curses.color_pair(4)) #just testing sth
    # lower_bar.addstr(((lower_bar.getmaxyx()[0]) - 1), 2, f"hl: {highlighted_item} max_len: {max_list_len}", curses.color_pair(4)) #just testing sth
    # lower_bar.addstr(((lower_bar.getmaxyx()[0]) - 3), 2, f"len: {list_len}", curses.color_pair(4)) #just testing sth

    if preview_file:
        try:
            with open(path, "r") as f:
                file_output = f.read()

            menu.clear()
            lines = file_output.split("\n")
            for index, line in enumerate(lines):
                start_index = preview_line
                last_index = preview_line + max_list_len
                y_pos = index - start_index
                line = line[0:(max_name_len)] + "..." if len(line) > max_name_len else line
                if index >= start_index and index <= last_index :
                    menu.addstr((y_pos + 1), 3, line, curses.color_pair(254))
            
            lines_string = f"Line: {preview_line}/{len(lines)}"
            lower_bar.clear()
            lower_bar.addstr(((lower_bar.getmaxyx()[0]) - 2), (lower_bar.getmaxyx()[1] - len(lines_string) - 2), f"{lines_string}", curses.color_pair(4))
            lower_bar.addstr(((lower_bar.getmaxyx()[0]) - 2), 2, f"Press ", curses.color_pair(4))
            lower_bar.addstr(((lower_bar.getmaxyx()[0]) - 2), 8, f"Shift + P", curses.color_pair(5) | curses.A_BOLD)
            lower_bar.addstr(((lower_bar.getmaxyx()[0]) - 2), 17, f" to close file preview.", curses.color_pair(4))

        except:
            lines = []
            pass

    lower_bar.refresh()
    menu.refresh()

    return (path, 0) if not preview_file else (path, len(lines))

def is_readable(path):

    try:
        with open(path, 'r') as f:
            f.read()
            return True
    except UnicodeError:
        return False

def preview_steering(key, preview_file, preview_line, preview_len, max_list_len):
    
    if preview_file:
        match key:
            case curses.KEY_DOWN:
                return [3, True] if (preview_line + max_list_len + 1) < preview_len else [0, True]
            case curses.KEY_UP:
                return [(-3), True] if preview_line > 0 else [0, True]
            case 80:
                return [(preview_line * (-1)), False]
            case _:
                return [0, True]
    else:
        return (0, preview_file)

def copy_paste_move(path, copy_path, key) -> str: #allows copy and move files using hotkeys
    
    new_path = ('/'.join(x.replace(' ', r'\ ') if ' ' in x else x for x in os.getcwd().split('/'))) + '/'
    sudo = True if (os.geteuid() == 0) else False
    
    match key:
        case 67: # Shift + C (copy)
            return f'{new_path}"{path}"'
        case 77: # Shift + M (move)
            os.system(f'sudo mv {copy_path} {new_path}' if sudo else f'mv {copy_path} {new_path}')
            return ""
        case 86: # Shift + V (paste)
            os.system(f'sudo cp {copy_path} {new_path}' if sudo else f'cp {copy_path} {new_path}')
            return ""

def delete_item(lower_bar, path, last_path, highlighted_item, list_len, delete_warning):

    highlight_change = 0

    if not delete_warning:
        lower_bar.addstr(((lower_bar.getmaxyx()[0]) - 2), 3, f'Delete "{path}" ?', curses.color_pair(4))
        return highlight_change, True, path
    
    if delete_warning and last_path == path:
        try:
            os.rmdir(path) if os.path.isdir(path) else os.remove(path)
            highlight_change = (-1) if highlighted_item == list_len else 0
        except PermissionError:
            lower_bar.clear()
            lower_bar.addstr(((lower_bar.getmaxyx()[0]) - 2), 3, "No permissions.", curses.color_pair(4))
            lower_bar.refresh()
        except:
            pass

    return highlight_change, False, ""

def steering(key, lower_bar, path, last_path, highlighted_item, last_index, current_page, items_pages, list_len, max_list_len, delete_warning) -> int: #allows to control app using keyboard

    lower_bar.clear()

    match key:
        case curses.KEY_UP:
            return (-1) if highlighted_item > 0 else 0
        case curses.KEY_DOWN:
            return 1 if highlighted_item < list_len else 0
        case curses.KEY_RIGHT:
            if current_page + 1 == items_pages:
                return last_index - highlighted_item + 1
            else:
                return (max_list_len + 1 ) if current_page < items_pages else 0
        case curses.KEY_LEFT:
            return (max_list_len + 1 ) * (-1) if current_page > 1 else 0
        case curses.KEY_BACKSPACE:
            return change_dir(lower_bar, "..", highlighted_item) if os.getcwd() != "/" else 0
        case 68: # Shift + D
            return delete_item(lower_bar, path, last_path, highlighted_item, list_len, delete_warning)[0] if highlighted_item != (last_index - max_list_len) else 0
        case 10: # Enter (submit)
            return (0 if not os.path.isdir(path) else change_dir(lower_bar, path, highlighted_item))
        case _: #kind of "else" in match case statement
            return 0

def check_highlight(highlighted_item, first_index, last_index) -> int: #function sets highlight in right place when user go to the end of page

    if highlighted_item > last_index:
        return last_index - highlighted_item
    elif highlighted_item < first_index:
        return first_index - highlighted_item
    else:
        return 0
    
def change_page(key, highlighted_item, current_page, items_pages, list_len, first_index, last_index, delete_warning) -> int: #function allows changing pages

    match key:
        case 10: #10 is ASCII Code of Enter key
            return ((current_page * (-1)) + 1)
        case curses.KEY_RIGHT:
            return 1 if current_page < items_pages else 0
        case curses.KEY_LEFT:
            return (-1) if current_page > 1 else 0
        case curses.KEY_DOWN:
            return 1 if highlighted_item > last_index else 0
        case curses.KEY_UP:
            return (-1) if highlighted_item < first_index else 0
        case curses.KEY_BACKSPACE:
            return (current_page * (-1)) + 1
        case _: #kind of "else" in match case statement
            return (-1) if items_pages > 1 and list_len == (first_index + 1) and delete_warning else 0
            
##### CLOSE FUNCTIONS #####

def close_functions(menu): #functions needed to be executed to close app propertly

    curses.nocbreak()
    menu.keypad(False)
    curses.echo()
    curses.endwin()
    curses.raw()
    os.system("reset")
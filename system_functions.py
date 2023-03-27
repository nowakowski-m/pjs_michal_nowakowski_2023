import curses   #for TUI, graphical terminal interface
import yaml     #support for yaml settings file
import os       #for manipulating system status, controling and reading files/dirs

##### OPENING FUNCTIONS #####

def start_things(stdscr, menu_shadow, menu): #just inits needed things for curses library usage in this app
    
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)

    curses.start_color()
    curses.init_color(1, 169, 184, 427) #blue window background
    curses.init_color(2, 75, 976, 769) #cyan app shadow
    curses.init_color(3, 918, 75, 569) #pink app background
    curses.init_color(4, 0, 0, 0) #black hotkeys tips background
    curses.init_color(254, 918, 75, 569) #pink bg for no item highlight
    curses.init_color(255, 75, 976, 769) #cyan item highlight
    curses.init_pair(1, curses.COLOR_BLACK, 1)
    curses.init_pair(2, curses.COLOR_BLACK, 2)
    curses.init_pair(3, curses.COLOR_BLACK, 3)
    curses.init_pair(4, curses.COLOR_WHITE, 4)
    curses.init_pair(254, curses.COLOR_BLACK, 254)
    curses.init_pair(255, curses.COLOR_BLACK, 255)

    stdscr.bkgd(curses.color_pair(1))
    stdscr.refresh()
    menu_shadow.bkgd(curses.color_pair(2))
    menu_shadow.refresh()
    menu.bkgd(curses.color_pair(3))
    menu.keypad(True)
    menu.refresh()

def screen_elements(stdscr): #initializing new windows and returns it
    margin, height, width, lines, cols = get_sizes()
    menu_shadow = curses.newwin(lines, cols, (margin + 1), ((2 * margin) + 2))
    menu = curses.newwin(lines, cols, margin, (2 * margin))
    max_list_len = int(height) - (3 * margin) - 1

    return menu_shadow, menu, max_list_len

def load_settings() -> list: #loading settings file and returns it values as lists
    with open('/home/nowakowski-m/Programowanie/Semestr 2/PJS2023/settings.yaml') as f:
        config = yaml.safe_load(f)

    user_settings = [x for x in config["user_settings"].values()]
    global_variables = [y for y in config["global_variables"].values()]

    return user_settings, global_variables

##### WINDOWS PARAMTERES #####

def get_sizes() -> int: #function create usefull sizes for app, like windows sizes
    margin = 4
    height, width = os.popen('stty size', 'r').read().split()
    lines = (int(height) - (2 * margin) - 1)
    cols = (int(width) - (4 * margin) - 2)

    return margin, height, width, lines, cols


def change_size(stdscr, menu_shadow, menu): #resizing windows, when terminal size changed
    margin, height, width, lines, cols = get_sizes()
    stdscr.resize(int(height), int(width))
    menu_shadow.resize(lines, cols)
    menu.resize(lines, cols)
    stdscr.refresh()
    menu_shadow.refresh()
    menu.refresh()

##### FILES SUPPORT #####

def list_items(show_hidden_items, max_list_len) -> list: #checking for items in current dir and prepares list for app needs

    items_list = [f'° No higher dirs.' if os.getcwd() == "/" else f'° Go back.']
    match show_hidden_items:
        case True:
            list_to_get = [f for f in os.listdir()]
        case False:
            list_to_get = [f for f in os.listdir() if not f.startswith('.')]

    if (len(list_to_get) + 1) > max_list_len:
        for name in list_to_get:
            
            items_list.append(f'𝔻 {name}' if os.path.isdir(name) else f'𝔽 {name}')
            
            if len(items_list) % max_list_len == 0:
                items_list.append(f'° Go back.')

    else:
        items_list.extend(f'𝔻 {name}' if os.path.isdir(name) else f'𝔽 {name}' for name in list_to_get)
            
    return items_list

def change_dir(path, highlighted_item) -> int: #function changing directory and returning position
    try:
        os.chdir(path)
        return (0 - highlighted_item)
    except PermissionError:
        #can add kind of warning shown at screen to inform user of no access
        return 0

##### MENU AND IT'S STEERING #####

def render_things(menu, show_hidden_items, highlighted_item, max_list_len, items_pages, current_page) -> str: #rendering current app status on screen

    menu.clear()

    first_index = max_list_len * (current_page - 1)
    last_index = first_index + max_list_len - 1

    for index, item in enumerate(list_items(show_hidden_items, max_list_len)):
        if index == highlighted_item:
            curr_color = curses.color_pair(255)

            if "𝔻" in item:
                path = item.split("𝔻")[1][1::]
            elif "°" in item:
                path = ".."
            else:
                path = item

        else:
            curr_color = curses.color_pair(254)

        y_pos = index - (max_list_len * (current_page - 1))

        if index == first_index and (index < last_index and index >= first_index):
            menu.addstr((y_pos + 1), 3, item, curr_color)

        elif index != first_index and (index < last_index and index >= first_index):
            menu.addstr((y_pos + 1), 5, item, curr_color)

    # test strings 
    # menu.addstr(((menu.getmaxyx()[0]) - 2), 2, f"Max_list_len: {max_list_len}", curses.color_pair(4)) #just testing sth
    # menu.addstr(((menu.getmaxyx()[0]) - 1), 2, f"Current page: {current_page}", curses.color_pair(4)) #just testing sth
    # menu.addstr(((menu.getmaxyx()[0]) - 3), 2, f"path: {path}", curses.color_pair(4)) #just testing sth
    menu.refresh()

    return path

def sterring(key, path, highlighted_item, current_page, items_pages, list_len, max_list_len) -> int: #allows to control app using keyboard

    match key:
        case curses.KEY_UP:
            return (-1) if highlighted_item > 0 else 0
        case curses.KEY_DOWN:
            return 1 if highlighted_item < list_len else 0
        case curses.KEY_RIGHT:
            return max_list_len if current_page < items_pages else 0
        case curses.KEY_LEFT:
            return max_list_len * (-1) if current_page > 1 else 0
        case 10: #10 is ASCII Code of Enter key
            return (0 if "𝔽" in path else change_dir(path, highlighted_item))
        case _: #kind of "else" in match case statement
            return 0

def change_page(key, current_page, items_pages, path):

    match key:
        case 10: #10 is ASCII Code of Enter key
            return ((current_page * (-1)) + 1 if "𝔽" not in path else 0)
        case curses.KEY_RIGHT:
            return 1 if current_page < items_pages else 0
        case curses.KEY_LEFT:
            return (-1) if current_page > 1 else 0
        case _: #kind of "else" in match case statement
            return 0
            
##### CLOSE FUNCTIONS #####

def close_functions(menu): #functions needed to be executed to close app propertly

    curses.nocbreak()
    menu.keypad(False)
    curses.echo()
    curses.endwin()
    curses.raw()
    os.system("reset")
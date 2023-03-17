import curses   #for TUI, graphical terminal interface
import yaml     #support for yaml settings file
import os       #for manipulating system status, controling and reading files/dirs

def load_settings() -> list: #loading settings file and returns it values as lists
    with open('settings.yaml') as f:
        config = yaml.safe_load(f)

    user_settings = [x for x in config["user_settings"].values()]
    global_variables = [y for y in config["global_variables"].values()]

    return user_settings, global_variables

def list_items(show_hidden_items) -> list: #checking for items in current dir and prepares list for app needs

    items_list = [f'° No higher dirs.' if os.getcwd() == "/" else f'° Go back.']
    match show_hidden_items:
        case True:
            list_to_get = [f for f in os.listdir()]
        case False:
            list_to_get = [f for f in os.listdir() if not f.startswith('.')]
    items_list.extend(f'𝔻 {name}' if os.path.isdir(name) else f'𝔽 {name}' for name in list_to_get)
            
    return items_list

def render_things(menu, show_hidden_items, highlighted_item) -> str: #rendering current app status on screen

    menu.clear()

    for index, item in enumerate(list_items(show_hidden_items)):
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

        if index == 0:
            menu.addstr((index + 1), 3, item, curr_color)
        else:
            menu.addstr((index + 1), 5, item, curr_color)

    menu.refresh()

    return path

def close_functions(menu): #functions needed to be executed to close app propertly

    curses.nocbreak()
    menu.keypad(False)
    curses.echo()
    curses.endwin()
    curses.raw()
    os.system("reset")

def get_sizes(stdscr) -> int: #function create usefull sizes for app, like windows sizes
    margin = 4
    # height, width = stdscr.getmaxyx()
    height, width = os.popen('stty size', 'r').read().split()
    lines = (int(height) - (2 * margin) - 1)
    cols = (int(width) - (4 * margin) - 2)

    return margin, height, width, lines, cols

def screen_elements(stdscr): #initializing new windows and returns it
    margin, height, width, lines, cols = get_sizes(stdscr)
    menu_shadow = curses.newwin(lines, cols, (margin + 1), ((2 * margin) + 2))
    menu = curses.newwin(lines, cols, margin, (2 * margin))

    return menu_shadow, menu

def change_size(stdscr, menu_shadow, menu): #resizing windows, when terminal size changed
    margin, height, width, lines, cols = get_sizes(stdscr)
    stdscr.resize(int(height), int(width))
    menu_shadow.resize(lines, cols)
    menu.resize(lines, cols)
    stdscr.refresh()
    menu_shadow.refresh()
    menu.refresh()

def change_dir(path, highlighted_item) -> int: #function changing directory and returning position
    try:
        os.chdir(path)
        return (0 - highlighted_item)
    except PermissionError:
        #can add kind of warning shown at screen to inform user of no access
        return 0

def sterring(key, path, show_hidden_items, highlighted_item) -> int: #allows to control app using keyboard
    
    match key:
        case curses.KEY_UP:
            return ((-1) if highlighted_item > 0 else 0)
        case curses.KEY_DOWN:
            return (1 if highlighted_item < (len(list_items(show_hidden_items)) - 1) else 0)
        case 10: #10 is ASCII Code of Enter key
            return (0 if "𝔽" in path else change_dir(path, highlighted_item))
        case _:
            return 0

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
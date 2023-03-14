import curses   #for TUI, graphical terminal interface
import os       #for manipulating system status, controling and reading files/dirs

def list_items() -> list: #checking for items in current dir and prepares list for app needs

    #this function is going to be extended with show hidden files option using bool
    #user will turn this option on or off using hotkey or app properties

    items_list = [f'° No higher dirs.' if os.getcwd() == "/" else f'° Go back.']
    no_hidden_list = [f for f in os.listdir() if not f.startswith('.')]
    items_list.extend(f'𝔻 {name}' if os.path.isdir(name) else f'𝔽 {name}' for name in no_hidden_list)
            
    return items_list

def render_things(menu, highlighted_item) -> str: #rendering current app status on screen

    menu.clear()

    for index, item in enumerate(list_items()):
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

def sterring(key, path, highlighted_item) -> int: #allows to control app using keyboard
    
    match key:
        case curses.KEY_UP:
            pos = (-1)
        case curses.KEY_DOWN:
            pos = 1
        case 10: #10 is ASCII Code of Enter key
            if "𝔽" in path:
                pos = 0
            else:
                os.chdir(path)
                pos = (0 - highlighted_item)
        case _:
            pos = 0

    return pos

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
#simple rgb scaller from 0-255 to 0-1000 due to curses rgb range 0-1000
#used to create "LAHIM", but not used in it itself

import os

def change_rgb_to_1000(rgb_ele) -> int:
    return round((int(rgb_ele)) / 255 * 1000)

def show_corrected() -> str:
    rgb_list = input_color.split(",")
    rgb_list = list(int(ele) for ele in rgb_list)
    corrected_list = list(map(change_rgb_to_1000, rgb_list))
    return f'REAL RGB: {rgb_list}\nCORRECTED RGB: {corrected_list}'

input_color = str(input("Type rgb color: "))
os.system('clear')
print(f'{show_corrected()}')
import os

def prev_dir():
    return os.chdir('..')

def marked_div(dirName):
    command = f'cd {dirName}'
    return os.system(command)

def list_items():
    whole_read = os.popen('file *').readlines()
    
    if (os.getcwd()) == "/":
        items_dict = {}
        item_index = 1

    else:
        items_dict = {1:"° Go back"}
        item_index = 2

    
    for lines in whole_read:

        line = lines.split(':')

        if 'directory' in line[1]:
            item_to_add = f'𝔻  {line[0]}'
        else:
            item_to_add = f'𝔽  {line[0]}'
        
        items_dict.update({item_index:item_to_add})

        item_index += 1
    
    return items_dict
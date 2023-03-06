import os

def prev_dir():
    return os.chdir('..')

def marked_div(dir_name):
    return os.chdir(dir_name)

def list_items():
    whole_read = os.popen('file *').readlines()
    
    if (os.getcwd()) == "/":
        items_dict = {1:"° No higher dirs"}

    else:
        items_dict = {1:"° Go back"}

    item_index = 2
    
    for lines in whole_read:

        line = lines.split(':')

        if ('directory' in line[1]) or ('symbolic link' in line[1]):
        # if ('directory' or 'symbolic link') in line[1]:
            item_to_add = f'𝔻  {line[0]}'
        else:
            item_to_add = f'𝔽  {line[0]}'
        
        items_dict.update({item_index:item_to_add})

        item_index += 1

    if ((len(items_dict)) == 2) and (("No" or "no") in ((os.popen('file *').readlines())[0])):
        items_dict = {1:"° Go back", 2:"Empty directory."}

    return items_dict
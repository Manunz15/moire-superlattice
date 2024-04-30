# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

import shutil

def copy_file(filename: str, path: str) -> None:
    """
    COPY FILE
    -------------------------------------------------------------------------
    Function for copying files from one directory to another. 

    Parameters
    ----------
    filename : string. The name of the file to be copied.

    path : string. The destination path where the file will be copied. 
    """
    
    shutil.copy2(filename, path)

def replace(filename: str, replacements: dict[str, str], final_filename: str = None) -> None:
    """
    REPLACE IN FILE
    -------------------------------------------------------------------------
    Function for replacing strings in a file with others. 

    Parameters
    ----------
    filename : string. The name of the file where the strings will be 
        replaced.
    
    replacements : dictionary mapping strings to strings. The keys are the 
        strings to be replaced, and the values are the strings that will 
        replace the keys. Each key must have only one corresponding value. 

        For example, with replacements = {'hello': 'hola', '15': '42'} 
        every occurrence of 'hello' in the file will be replaced with 'hola', 
        and every occurrence '15' will be replaced with '42'.
    
    final_filename: string. The name that the modified file will have. If not
        specified, the original file will be overwritten.
    """
    if final_filename is None:
        final_filename = filename
 
    # open file
    with open(filename, 'r') as f:
        lines = f.readlines()

    # replace strings
    for index, line in enumerate(lines):
        for old, new in replacements.items():
            if old in line:
                line = line.replace(str(old), str(new))
                lines[index] = line

    # save file
    with open(final_filename, 'w') as f:
        f.writelines(lines) 

def remove(filename: str, start_key: str, final_filename: str = None) -> None:
    '''
    REMOVE LINES
    -------------------------------------------------------------------------
    Function for removing lines from a file until a 'start_key' appears.

    Parameters
    ----------
    filename : string. The name of the file to edit
    
    start_key: string. The new file will start with the line where this string
        first appear in the original file. For example, if 
        start_key = 'string' the edited version of this description would
        start with 'filename: string. The name ect...', the previous lines
        will be deleted.
    
    final_filename: string. The name that the modified file will have. If not
        specified, the original file will be overwritten.
    '''
    # initialization
    save = False
    new_lines = []
    if final_filename is None:
        final_filename = filename

    # open file
    with open(filename, 'r') as f:
        lines = f.readlines()

    # save lines
    for line in lines:
        if start_key in line:
            save = True
        if save:
            new_lines.append(line)

    # save file
    with open(final_filename, 'w') as f:
        f.writelines(new_lines) 
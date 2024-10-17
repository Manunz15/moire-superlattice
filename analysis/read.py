# Lorenzo Manunza, Università degli Studi di Cagliari, March 2024

import pandas as pd
import re

def read_box(filename: str) -> list[tuple[float]]:
    box_lines = 0
    box = []

    # read file
    with open(filename, 'r') as f:
        for line in f:
            # print(line)
            if box_lines:
                box_lines -= 1
                b = tuple(map(float, re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', line)))
                box.append(b)
                if len(box) == 3:
                    return box

            # box line
            if 'BOX BOUNDS' in line:
                box_lines = 3
        else:
            raise NameError(f'There are not boxes in the file: {filename}')

def read_log(filename: str) -> pd.DataFrame:
    # initialization
    read: bool = False
    run_count: int = 0

    # read file
    with open(filename, 'r') as f:
        for line in f:
            # columns line
            if 'Step' in line:
                read: bool = True
                run_count += 1

                # first columns line
                if run_count == 1:
                    DATA: list[float] = []
                    COLUMNS: list[float] = line.split()

            # stop reading
            elif 'Loop time of ' in line:
                read: bool = False
                
            # read data
            elif read:
                DATA.append(list(map(float, line.split())))

    return pd.DataFrame(DATA, columns = COLUMNS)
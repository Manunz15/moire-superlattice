# Lorenzo Manunza, Università degli Studi di Cagliari, March 2024

import pandas as pd
import re

def read_box(filename: str) -> list[tuple[float]]:
    # read file
    with open(filename, 'r') as f:
        for line in f:
            # box line
            if 'orthogonal box' in line:
                b = list(map(float, re.findall('[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', line)))
                box = [(b[0], b[3]), (b[1], b[4]), (b[2], b[5])]
                return box
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
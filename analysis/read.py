# Lorenzo Manunza, Università degli Studi di Cagliari, March 2024

import numpy as np
import pandas as pd
import time

class ReadData:
    def __init__(self):
        pass
    
    def find_columns(self, file):
        for line in file:
            if 'ITEM: ATOMS' in line:
                COLUMNS = line.split()[2:]

        COLUMNS.insert(0, 'timestep')

        return COLUMNS
    
    def append(self, DF: pd.DataFrame, VALUES: np.array, timestep: int, COLUMNS: list):
        # append data
        VALUES = np.array(VALUES)
        VALUES = np.insert(VALUES, 0, np.full(fill_value = timestep, shape = len(VALUES)), axis = 1).astype(float)
        ts_DF = pd.DataFrame(VALUES, columns = COLUMNS).astype({'timestep': int, 'id': int, 'type': int}).sort_values(by = 'id')
        DF = pd.concat([DF, ts_DF], ignore_index = True)

        return DF
    
    def read_trj(self, filename: str = None):

        # initialization
        read = False
        timestep = 0
        previous_line = ''
        VALUES = []

        # create dataframe
        f = open(filename, 'r')
        COLUMNS = self.find_columns(f)
        DF = pd.DataFrame(columns = COLUMNS)
        f.close()

        # read data
        f = open(filename, 'r')
        for line in f:
            
            if 'ITEM: TIMESTEP' in previous_line:
                timestep = int(line)
                VALUES = []
                if not timestep % 1000:
                    print(timestep)

            if 'ITEM: TIMESTEP' in line and read:
                read = False
                DF = self.append(DF, VALUES, timestep = timestep, COLUMNS = COLUMNS)

            if read:
                VALUES.append(line.split())

            if 'ITEM: ATOMS' in line:
                read = True

            previous_line = line

        f.close()
        
        # last timestep
        DF = self.append(DF, VALUES, timestep = timestep, COLUMNS = COLUMNS)

        return DF

    def read_log(self, filename: str, variables: list[str]):
        
        # initialization
        read = False
        var_line = False

        DATA = []

        with open(filename) as f:
            for line in f:
                # stop reading
                if 'Loop time of ' in line:
                    read = False

                # read data
                if read:
                    DATA.append([float(line.split()[i]) for i in COLUMNS])

                # variables
                if var_line:
                    var_line = False
                    read = True
                    COLUMNS = [index for index, var in enumerate(line.split()) if var in variables]

                # next line is columns names
                if 'Per MPI rank memory allocation (min/avg/max)' in line:
                    var_line = True

        return np.array(DATA)

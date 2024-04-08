# Lorenzo Manunza, Università degli Studi di Cagliari, March 2024

import numpy as np
import pandas as pd

class HexLattice:
    def __init__(self):
        self.angle = np.deg2rad(60)
        self.columns = ['x', 'y']
    
    def create(self, step: float = 1, dim: tuple = (1, 1), atom_types: int = 1):
        rows, cols = dim

        # types of atoms
        if atom_types not in [1, 2]:
            raise ValueError(f'Number of types of atoms must be 1 or 2, not {atom_types}')

        # initialization
        STEP = step
        ANGLE = self.angle
        COLUMNS = self.columns

        x_STEP = STEP * 2 * (1 + np.cos(ANGLE))
        y_STEP = STEP * 2 * np.sin(ANGLE)

        BASE = np.array([[0,0],
                        [STEP * np.cos(ANGLE), STEP * np.sin(ANGLE)], 
                        [STEP * (1 + np.cos(ANGLE)), STEP * np.sin(ANGLE)],
                        [STEP * (1 + 2 * np.cos(ANGLE)), 0]])

        # create lattice
        DFs = []
        for nx in range(rows):
            for ny in range(cols):
                new_ATOMS = BASE.copy()
                new_ATOMS[:, 0] += x_STEP * nx
                new_ATOMS[:, 1] += y_STEP * ny

                DFs.append(pd.DataFrame(new_ATOMS, columns = COLUMNS))

        DF = pd.concat(DFs, ignore_index = True)

        # id and z columns
        num_atoms = len(DF)

        z_COL = np.zeros(num_atoms)
        id_COL = np.arange(1, num_atoms + 1)

        # type of atom column
        type_list = list(range(1, atom_types + 1)) * (num_atoms // atom_types)

        if len(type_list) == num_atoms:
            type_COL = np.array(type_list)
        else:
            type_COL = np.ones(num_atoms, dtype = int)

        DF.insert(0, 'id', id_COL, True)
        DF.insert(1, 'type', type_COL, True)
        DF.insert(4, 'z', z_COL, True)

        return DF

if __name__ == '__main__':
    hex = HexLattice()
    hex_DF = hex.create(step = 2.1, num_atoms = 1200, dim = (15, 21))

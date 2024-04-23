# Lorenzo Manunza, Università degli Studi di Cagliari, March 2024

from lattice.lattice import Lattice

import numpy as np
import pandas as pd

class HexLattice(Lattice):
    def __init__(self, lattice: str, dim: tuple = None, name: str = None) -> None:
        super().__init__(lattice = lattice, name = name)
    
        if dim:
            self.create(dim = dim)

    def create(self, dim: tuple) -> pd.DataFrame:
        # initialization and unit cell
        ANGLE: float = np.deg2rad(60)
        COLUMNS: list[str] = ['x', 'y']
        NUM_TYPES = len(self.atom_types)
        
        x_STEP = self.step * 2 * (1 + np.cos(ANGLE))
        y_STEP = self.step * 2 * np.sin(ANGLE)

        UNIT_CELL = np.array([[0,0],
                        [self.step * np.cos(ANGLE), self.step * np.sin(ANGLE)], 
                        [self.step * (1 + np.cos(ANGLE)), self.step * np.sin(ANGLE)],
                        [self.step * (1 + 2 * np.cos(ANGLE)), 0]])
        
        # create lattice
        ATOMS_LIST = []
        rows, cols = dim
        for nx in range(rows):
            for ny in range(cols):
                new_CELLS = UNIT_CELL.copy()
                new_CELLS[:, 0] += x_STEP * nx
                new_CELLS[:, 1] += y_STEP * ny

                ATOMS_LIST.append(pd.DataFrame(new_CELLS, columns = COLUMNS))

        ATOMS = pd.concat(ATOMS_LIST, ignore_index = True)

        # id and z columns
        num_atoms = len(ATOMS)

        z_COL = np.zeros(num_atoms)
        id_COL = np.arange(1, num_atoms + 1)

        # type of atom column
        type_list = list(range(1, NUM_TYPES + 1)) * (num_atoms // NUM_TYPES)

        if len(type_list) == num_atoms:
            type_COL = np.array(type_list)
        else:
            type_COL = np.ones(num_atoms, dtype = int)

        ATOMS.insert(0, 'id', id_COL, True)
        ATOMS.insert(1, 'type', type_COL, True)
        ATOMS.insert(4, 'z', z_COL, True)

        self.add(atoms = ATOMS)
# Lorenzo Manunza, Università degli Studi di Cagliari, March 2024

from lattice.lattice import Lattice
from lattice.add_layers import add_layers

import numpy as np
import pandas as pd

class HexLattice(Lattice):
    def __init__(self, lattice: str, name: str = None, dim: tuple = None, angle: float = None, filename: str = None) -> None:
        super().__init__(lattice = lattice, name = name, filename = filename)

        if angle and dim:
            self.bilayer(angle = angle, dim = dim)
        elif dim:
            self.create(dim = dim)

    def create(self, dim: tuple) -> None:
        # initialization and unit cell
        ANGLE: float = np.deg2rad(60)
        COLUMNS: list[str] = ['x', 'y']
        NUM_TYPES = len(self.atom_types)
        
        x_STEP = self.step * 2 * (1 + np.cos(ANGLE))
        y_STEP = self.step * 2 * np.sin(ANGLE)

        UNIT_CELL = np.array([[- self.step * (1 + 2 * np.cos(ANGLE)) / 2,0],
                        [self.step * np.cos(ANGLE)- self.step * (1 + 2 * np.cos(ANGLE)) / 2, self.step * np.sin(ANGLE)], 
                        [self.step * (1 + np.cos(ANGLE))- self.step * (1 + 2 * np.cos(ANGLE)) / 2, self.step * np.sin(ANGLE)],
                        [self.step * (1 + 2 * np.cos(ANGLE)) / 2, 0]])
        
        # create lattice
        ATOMS_LIST = []
        rows, cols = dim
        for nx in range(- rows // 2, rows // 2 + 1):
            for ny in range(- cols // 2, cols // 2 + 1):
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

    def bilayer(self, angle: float, dim: tuple[int]) -> None:
        # initialization
        n: int = int(- 0.5 + 0.5 / (np.sqrt(3) * np.tan(np.deg2rad(angle / 2))))
        half_angle: float = float(np.arctan(1 / (np.sqrt(3) * (2 * n + 1))))
        angle: float = np.rad2deg(half_angle * 2)
        
        unit_cell = HexLattice(self.lattice, dim = (3 * n, 5 * n))
        unit_cell.add(add_layers(unit_cell, angle).atoms)

        # unit cell
        L: float = float(self.step * (3 * np.cos(half_angle) * (2 * n + 1) + np.sqrt(3) * np.sin(half_angle)) / 2)
        min_x: float = - L / 2
        max_x: float = L / 2
        min_y: float = - np.sqrt(3) * L / 2
        max_y: float = np.sqrt(3) * L / 2
        cut_box: list[tuple] = [(min_x, min_y), (max_x, max_y)]

        # cut
        unit_cell.cut(cut_box)
        unit_cell.rotate(90)

        # create lattice from unit cell
        ATOMS_LIST = []
        COLUMNS = ['type', 'x', 'y', 'z']
        UNIT_CELL = np.zeros([len(unit_cell.atoms), 4])
        for index, col in enumerate(COLUMNS):
            UNIT_CELL[:, index] = unit_cell.atoms[col].to_numpy()
            
        x_STEP = 2 * UNIT_CELL[:, 1].max()
        y_STEP = 2 * UNIT_CELL[:, 2].max()

        rows, cols = dim
        for nx in range(rows):
            for ny in range(cols):
                new_CELLS = UNIT_CELL.copy()
                new_CELLS[:, 1] += x_STEP * nx
                new_CELLS[:, 2] += y_STEP * ny

                ATOMS_LIST.append(pd.DataFrame(new_CELLS, columns = COLUMNS))

        ATOMS = pd.concat(ATOMS_LIST, ignore_index = True)
        ATOMS.insert(0, 'id', np.arange(1, len(ATOMS) + 1), True)
        # type to int
        ATOMS['type'] = ATOMS['type'].to_numpy().astype(int)

        self.add(ATOMS)
        self.create_box(pad = [0, 0, 1e4])
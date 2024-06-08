# Lorenzo Manunza, Università degli Studi di Cagliari, March 2024

from lattice.lattice import Lattice
from lattice.add_layers import add_layers

import numpy as np
import pandas as pd
from typing import Any
    
class HexLattice(Lattice):
    def __init__(self, lattice: str, dim: tuple[int] = None, angle: float = None, name: str = None, filename: str = None) -> None:
        super().__init__(lattice = lattice, name = name, filename = filename)
        self.create_unit_cell()

        if not angle:
            self.create_monolayer(dim)
        else:
            self.create_bilayer(dim, angle)

    @staticmethod
    def moire_angle(angle: float) -> Any:
        n: int = int(- 0.5 + 0.5 / (np.sqrt(3) * np.tan(np.deg2rad(angle / 2))))
        half_angle: float = float(np.arctan(1 / (np.sqrt(3) * (2 * n + 1))))
        deg_angle: float = np.rad2deg(half_angle * 2)

        return n, half_angle, deg_angle

    def create_unit_cell(self) -> None:
        # initialization
        ANGLE: float = np.deg2rad(60)

        self.x_STEP = self.step * 2 * (1 + np.cos(ANGLE))
        self.y_STEP = self.step * 2 * np.sin(ANGLE)

        self.unit_cell = np.array([[- self.step * (1 + 2 * np.cos(ANGLE)) / 2,0],
                        [self.step * np.cos(ANGLE)- self.step * (1 + 2 * np.cos(ANGLE)) / 2, self.step * np.sin(ANGLE)], 
                        [self.step * (1 + np.cos(ANGLE))- self.step * (1 + 2 * np.cos(ANGLE)) / 2, self.step * np.sin(ANGLE)],
                        [self.step * (1 + 2 * np.cos(ANGLE)) / 2, 0]])
        
    def duplicate_cell(self, cell: np.array, step: tuple[float], bounds: list[tuple[int]], columns: list[str], indexes: tuple[int] = (0, 1)) -> list[np.array]:
        # duplicate cell
        ATOMS_LIST = []
        (xi, xf), (yi, yf) = bounds
        for nx in range(xi, xf):
            for ny in range(yi, yf):
                new_CELL = cell.copy()
                new_CELL[:, indexes[0]] += step[0] * nx
                new_CELL[:, indexes[1]] += step[1] * ny

                ATOMS_LIST.append(new_CELL)

        ATOMS = pd.concat([pd.DataFrame(cell, columns = columns) for cell in ATOMS_LIST], ignore_index = True)

        return ATOMS
    
    def create_monolayer(self, dim: tuple[int]) -> None:
        # initialize
        rows, cols = dim
        bounds = [(- rows // 2, rows // 2 + 1), (- cols // 2, cols // 2 + 1)]
        ATOMS = self.duplicate_cell(self.unit_cell, (self.x_STEP, self.y_STEP), bounds, ['x', 'y'])
        
        # id and z columns
        num_atoms: int = len(ATOMS)
        zeros_COL: np.array = np.zeros(num_atoms)
        ones_COL: np.array = np.ones(num_atoms)
        id_COL: np.array = np.arange(1, num_atoms + 1)

        # atoms type column
        type_list = list(range(1, self.num_types + 1)) * (num_atoms // self.num_types)
        if len(type_list) == num_atoms:
            type_COL = np.array(type_list)
        else:
            type_COL = np.ones(num_atoms, dtype = int)

        # insert columns
        ATOMS.insert(0, 'id', id_COL, True)
        ATOMS.insert(1, 'type', type_COL, True)
        ATOMS.insert(4, 'z', zeros_COL, True)

        if self.full:
            ATOMS.insert(1, 'molecule', ones_COL.astype(int), True)
            ATOMS.insert(3, 'q', zeros_COL, True)

        self.add(ATOMS)

    def create_bilayer(self, dim: tuple[int], angle: float) -> None:
        # initialization
        n, half_angle, deg_angle = self.moire_angle(angle)
        
        # moire cell
        moire_cell = HexLattice(self.lattice, dim = (3 * n, 5 * n))
        moire_cell.add(add_layers(moire_cell, deg_angle).atoms)

        # cutting moire cell
        L: float = float(self.step * (3 * np.cos(half_angle) * (2 * n + 1) + np.sqrt(3) * np.sin(half_angle)) / 2)
        min_x, max_x, min_y, max_y = - L / 2,  L / 2, - np.sqrt(3) * L / 2, np.sqrt(3) * L / 2
        cut_box: list[tuple[float]] = [(min_x, min_y), (max_x + 1e-4, max_y + 1e-4)]
        moire_cell.cut(cut_box)
        moire_cell.rotate(90)
        
        # new cell
        x_STEP = 2 * max_y
        y_STEP = 2 * max_x
        COLUMNS = moire_cell.atoms.columns[1:]
        UNIT_CELL = np.zeros([len(moire_cell.atoms), len(COLUMNS)])
        for index, col in enumerate(COLUMNS):
            UNIT_CELL[:, index] = moire_cell.atoms[col].to_numpy()

        # duplicate
        rows, cols = dim
        ATOMS = self.duplicate_cell(UNIT_CELL, (x_STEP, y_STEP), [(0, rows), (0, cols)], COLUMNS, (-3, -2))
        ATOMS.insert(0, 'id', np.arange(1, len(ATOMS) + 1).astype(int), True)
        ATOMS['type'] = ATOMS['type'].to_numpy().astype(int)
        if self.full:
            ATOMS['molecule'] = ATOMS['molecule'].to_numpy().astype(int)

        # save
        self.add(ATOMS)
        self.box = [(min_y, rows * x_STEP + min_y), (min_x, cols * y_STEP + min_x), (-1e4, 1e4)]
        self.centering()        
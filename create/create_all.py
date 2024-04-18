# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from create.hex import HexLattice
from create.second_layer import add_second_layer
from create.box import create_box
from data.write import WriteAtoms
from data.plot import PlotCrystal
from utils.today import today
from utils.file import File
from utils.path import Path
from utils.materials import lattices

import pandas as pd

class CreateAll:
    def __init__(self, lattice: str, filenames: list[str]) -> None:
        # properties
        self.lattice = lattice
        self.step = lattices[lattice]['step']
        self.z_step = lattices[lattice]['z_step']
        self.atoms = lattices[lattice]['atoms']

        # settings
        self.filenames = filenames

    def create_all(self, dir_name: str, DIMS: list[tuple], ANGLES: list[float] = None, *, plot: bool = False) -> None:
        # iterate for shape
        for dim in DIMS:
            DF = HexLattice().create(step = self.step, dim = dim, atom_types = 1)
            dim_dir = '' if len(DIMS) == 1 else f'dim_{dim[0]}x{dim[1]}'

            # if angles are specified
            if ANGLES:
                for angle in ANGLES:
                    rot_DF = add_second_layer(DF, angle = angle, trasl = [0, 0, self.z_step])
                    angle_dir = '' if len(ANGLES) == 1 else f'angle_{angle:.1f}'
                    path = '/'.join([dir_name, angle_dir, dim_dir])
                    self.save(rot_DF, path, plot)
            
            # if angles are NOT specified
            else:
                path = '/'.join([dir_name, dim_dir])
                self.save(DF, path, plot)

    def save(self, DF: pd.DataFrame, path: str, plot: bool) -> None:
        # box
        box = create_box(DF, delta = [self.step, self.step, 2000])
        replacements = {'x_1i': round(box[0][0], 3),
                'x_1f': round((box[0][1] - box[0][0]) / 2, 3),
                'x_2i': round((box[0][1] - box[0][0]) / 2 + 0.1, 3),
                'x_2f': round(box[0][1], 3)}

        # save
        path = Path(path = [self.lattice, path])
        print(path.path)
        path.copy(filenames = self.filenames)
        File().replace(filename = '/'.join([path.path,'in.CONDUCTIVITY']), replacements = replacements)
        WriteAtoms().write(DF = DF, atoms = self.atoms, filename = f'{path.path}/atoms.dat', 
                title = f'Lorenzo Manunza {today()}', box = box)
        
        # plot
        if plot:
            PlotCrystal().plot_2d([DF])
# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from create.hex import HexLattice
from create.box import create_box
from create.second_layer import add_second_layer
from data.plot import PlotCrystal
from data.write import WriteAtoms
from utils.settings import*
from utils.path import Path
from utils.today import today

import numpy as np
import os

# initialization
lattice = 'graphene'
path = Path(path = [lattice, 'best_method'])
files = ['/'.join(['lammps', lattice, 'CH.airebo']),
         '/'.join(['lammps', lattice, 'in.TO_300K'])]

# properties
step = lattices[lattice]['step']
atoms = lattices[lattice]['atoms']
square_width, height = 12, 21

# methods
ANGLES = [0, 10]
SHAPES = [(4, 6), (5, 6)]

# ANGLES = np.concatenate((np.arange(0, 2, 0.1), np.arange(2, 10), np.arange(10, 50, 5)))
# SHAPES = [(width, height) for width in range(square_width, height)]

for shape in SHAPES:
    # create new path
    print(f'{shape[0]}x{shape[1]}')
    new_path = Path(dir = path.path, path = [f'{lattice}{shape[0]}x{shape[1]}'])
    
    # create first layer
    hex_DF = HexLattice().create(step = step, dim = shape)

    for angle in ANGLES:
        # create dir
        dir_path = new_path.create_dir(dir = f'Angle{angle:.1f}', files = files)
        path_to_save = '/'.join([dir_path, 'atoms.dat'])

        # create second layer
        DF = add_second_layer(hex_DF, angle = angle, trasl = [0, 0, 3.3])
        box = create_box(DF, delta = [2, 2, 1000])

        # save atoms
        WriteAtoms().write(DF = DF, atoms = atoms, filename = path_to_save, 
                           title = f'Lorenzo Manunza {today()}', box = box)

        # PlotCrystal().plot_2d([DF])

        # only when running
        os.system('conda activate my-lammps')
        os.system('export OMP_NUM_THREADS=1')
        os.system(f'cd {dir_path}')
        os.system(f'mpirun -np 56 lmp -in in.TO_300K')
        os.system('conda deactivate')

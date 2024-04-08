from create.hex import HexLattice
from create.box import create_box
from create.second_layer import add_second_layer
from data.plot import PlotCrystal
from utils.settings import*
from utils.path import Path

import numpy as np

# initialization
lattice = 'graphene'
files = ['/'.join(['lammps', lattice, 'CH.airebo']),
         '/'.join(['lammps', lattice, 'in.TO_300K'])]

# properties
step = lattices[lattice]['step']
atoms = lattices[lattice]['atoms']
square_width, height = 12, 21

path = Path(path = [lattice, 'best_method'])
path.create_dir(dir = 'test', files = files)
print(path)

# methods
# ANGLES = np.concatenate((np.arange(0, 2, 0.1), np.arange(2, 10), np.arange(10, 50, 5)))
# SHAPES = [(width, height) for width in range(square_width, height)]

# for shape in SHAPES:
#     hex_DF = HexLattice().create(step = step, dim = shape)
    
#     for angle in ANGLES:
#         DF = add_second_layer(hex_DF, angle = angle, trasl = [0, 0, 3.3])

#         print(f'{lattice}{shape[0]}x{shape[1]}-{angle}')
#         # box = create_box(hex_DF, delta = [step, step, 1000])
#         box = create_box(DF, delta = [2, 2, 1000])
#         PlotCrystal().plot_2d([DF], angle = round(angle, 1))
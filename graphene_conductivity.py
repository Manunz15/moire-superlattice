# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from create.hex import HexLattice
from create.second_layer import add_second_layer
from create.box import create_box
from data.write import WriteAtoms
from data.plot import PlotCrystal
from utils.today import today
from utils.modify_file import modify_file
from utils.path import Path
from utils.materials import*

import numpy as np

lattice = 'graphene'
dir_name = 'conductivity'
files = ['/'.join(['lammps', lattice, 'CH.airebo']),
         '/'.join(['lammps', lattice, 'in.CONDUCTIVITY'])]

# properties
step = lattices[lattice]['step']
atoms = lattices[lattice]['atoms']

DF = HexLattice().create(step = step, dim = (121, 105), atom_types = 1)
box = create_box(DF, delta = [step, step, 2000])
PlotCrystal().plot_2d([DF])

changes = {'x_1i': round(box[0][0], 3),
        'x_1f': round((box[0][1] - box[0][0]) / 2, 3),
        'x_2i': round((box[0][1] - box[0][0]) / 2 + 0.1, 3),
        'x_2f': round(box[0][1], 3)}

# save
path = Path(path = [lattice, dir_name])
path.copy(files = files)
modify_file(filename = '/'.join([path.path,'in.CONDUCTIVITY']), changes = changes)
WriteAtoms().write(DF = DF, atoms = atoms, filename = f'../simulations/{lattice}/{dir_name}/atoms.dat', 
            title = f'Lorenzo Manunza {today()}', box = box)
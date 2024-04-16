# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from create.hex import HexLattice
from create.second_layer import add_second_layer
from create.box import create_box
from data.write import WriteAtoms
from data.plot import PlotCrystal
from utils.today import today
from utils.file import File
from utils.path import Path
from utils.materials import*

import numpy as np

lattice = 'graphene'
dir_name = 'conductivity_double_layer'
angle = 1.1
filenames = ['/'.join(['lammps', lattice, 'CH.airebo']),
         '/'.join(['lammps', lattice, 'in.CONDUCTIVITY'])]

# properties
step = lattices[lattice]['step']
atoms = lattices[lattice]['atoms']

hex_DF = HexLattice().create(step = step, dim = (121, 105), atom_types = 1)

ANGLES = np.arange(0, 2.1, 0.1)
for angle in ANGLES:
    print(round(angle, 2))
    DF = add_second_layer(hex_DF, angle = angle, trasl = [0, 0, 3.3])
    box = create_box(DF, delta = [step, step, 2000])
    # PlotCrystal().plot_2d([DF])

    replacements = {'x_1i': round(box[0][0], 3),
            'x_1f': round((box[0][1] - box[0][0]) / 2, 3),
            'x_2i': round((box[0][1] - box[0][0]) / 2 + 0.1, 3),
            'x_2f': round(box[0][1], 3)}

    # save
    path = Path(path = [lattice, dir_name, f'Angle{angle:.1f}'])
    path.copy(filenames = filenames)
    File().replace(filename = '/'.join([path.path,'in.CONDUCTIVITY']), replacements = replacements)
    WriteAtoms().write(DF = DF, atoms = atoms, filename = f'../simulations/graphene/{dir_name}/Angle{angle:.1f}/atoms.dat', 
                title = f'Lorenzo Manunza {today()}', box = box)
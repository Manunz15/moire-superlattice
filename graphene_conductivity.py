# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from create.create_all import CreateAll

import numpy as np

lattice = 'graphene'
filenames = ['/'.join(['lammps', lattice, 'CH.airebo']),
         '/'.join(['lammps', lattice, 'in.CONDUCTIVITY'])]

height = 105

dir_name = 'conductivity_final'
DIMS = [(width, height) for width in range(80, 160, 10)]
ANGLES = [0.0, 0.5, 1.0, 1.05, 1.1, 1.15, 1.2, 1.5]
CreateAll(lattice, filenames, dir_name, DIMS, ANGLES)
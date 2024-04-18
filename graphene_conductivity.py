# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from create.create_all import CreateAll

import numpy as np

lattice = 'graphene'
filenames = ['/'.join(['lammps', lattice, 'CH.airebo']),
         '/'.join(['lammps', lattice, 'in.CONDUCTIVITY'])]

height = 105

# only one layer
dir_name = 'conductivity_shapes'
DIMS = [(width, height) for width in range(80, 200, 5)]
CreateAll(lattice, filenames).create_all(dir_name, DIMS)

# two layers
dir_name = 'conductivity_angles'
DIMS = [(121, height)]
ANGLES = list(np.arange(0, 2.1, 0.1))
CreateAll(lattice, filenames).create_all(dir_name, DIMS, ANGLES)
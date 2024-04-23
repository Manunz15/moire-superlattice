# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from lattice import create_all

lattice = 'graphene'

# height = 105
# dir_name = 'conductivity_final'
# DIMS = [(width, height) for width in range(80, 160, 10)]
# ANGLES = [0.0, 0.5, 1.0, 1.05, 1.1, 1.15, 1.2, 1.5]
# create_all(lattice = lattice, DIMS = DIMS, ANGLES = ANGLES, dir_name = dir_name, lammps = 'in.CONDUCTIVITY')

create_all(lattice = lattice, DIMS = (120, 100), dir_name = 'test_conductivity')
# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from lattice import create_all

lattice = 'graphene'

# single layer
create_all(lattice = lattice, DIMS = (120, 100), dir_name = 'conductivity_test')

# different shapes
height = 105
DIMS = [(width, height) for width in range(80, 205, 5)]
create_all(lattice = lattice, DIMS = DIMS, dir_name = 'conductivity_shapes_final')

# two layers
height = 105
DIMS = [(width, height) for width in range(80, 160, 10)]
ANGLES = [0.0, 0.5, 1.0, 1.05, 1.1, 1.15, 1.2, 1.5]
create_all(lattice = lattice, DIMS = DIMS, ANGLES = ANGLES, dir_name = 'conductivity_angles_final')

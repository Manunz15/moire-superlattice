# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from utils import create_all

lattice = 'graphene'

# different shapes
# height = 105
# DIMS = [(width, height) for width in range(80, 205, 5)]
# create_all(lattice = lattice, DIMS = DIMS, dir_name = 'conductivity_shapes_final')

# two layers
height = 105
DIMS = [(width, height) for width in range(60, 160, 20)]
ANGLES = [angle / 100 for angle in range(100, 120 + 1)]
create_all(lattice = lattice, DIMS = DIMS, ANGLES = ANGLES, dir_name = 'conductivity_angles')

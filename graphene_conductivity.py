# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from utils import create_all

lattice = 'graphene'

# different shapes
height = 100
DIMS = [(width, height) for width in range(60, 140 + 1, 20)]
create_all(lattice = lattice, DIMS = DIMS, dir_name = 'conductivity_single_layer')

# two layers
height = 100
DIMS = [(width, height) for width in range(60, 140 + 1, 20)]
ANGLES = [angle / 10 for angle in range(0, 15 + 1)]
# ANGLES = [angle / 100 for angle in range(100, 120 + 1)]
create_all(lattice = lattice, DIMS = DIMS, ANGLES = ANGLES, dir_name = 'conductivity_angles')

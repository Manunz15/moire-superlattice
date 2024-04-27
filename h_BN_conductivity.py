# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from utils import create_all

lattice = 'h-BN'

# different shapes
height = 100
DIMS = [(width, height) for width in range(80, 200 + 1, 20)]
create_all(lattice = lattice, DIMS = DIMS, dir_name = 'conductivity_shapes')

# two layers
height = 100
DIMS = [(width, height) for width in range(60, 160, 20)]
ANGLES = [angle / 100 for angle in range(100, 120 + 1)]
create_all(lattice = lattice, DIMS = DIMS, ANGLES = ANGLES, dir_name = 'conductivity_angles')
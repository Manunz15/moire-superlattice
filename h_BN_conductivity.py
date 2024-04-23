# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from lattice import create_all

# dim and angle
dim: tuple = (12, 20)

# create and plot
create_all(lattice = 'h-BN', dir_name = 'test', DIMS = dim, lammps = 'in.TO_300K', plot = True)
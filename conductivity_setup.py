# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from lattice import create_all

# initialization
lammps = 'in.SETUP_CONDUCTIVITY'
height = 100
DIMS = [(width, height) for width in range(60, 140 + 1, 20)]

# graphene
lattice = 'graphene'
create_all(lattice = lattice, DIMS = DIMS, dir_name = 'conductivity_setup', lammps = lammps)

# h-BN
lattice = 'h-BN'
create_all(lattice = lattice, DIMS = DIMS, dir_name = 'conductivity_setup', lammps = lammps)
create_all(lattice = lattice, DIMS = DIMS, dir_name = 'conductivity_setup_inverted', 
           lammps = lammps, interchange = True)
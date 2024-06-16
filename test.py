# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from lattice import HexLattice, add_layers

lt = HexLattice('ILP-graphene', dim = (1, 1), angle = 1.5)
lt.write_lammps('atoms.dat')
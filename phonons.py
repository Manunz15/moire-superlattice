# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from lattice import HexLattice

# create and plot
graphene = HexLattice('graphene', dim = (1, 1), angle = 1.1)
# graphene.write_lammps('../phonons/graphene/first_try/atoms.dat')
graphene.write_alm('test')
# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from lattice import HexLattice, add_layers

hbn = HexLattice('h-BN', dim = (60, 100))
hbn.write_lammps('../simulations/h-BN/test_gap/atoms.dat')

double_hbn = add_layers(hbn)
double_hbn.write_lammps('../simulations/h-BN/test_double_gap/atoms.dat')
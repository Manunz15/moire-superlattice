# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from lattice import HexLattice, add_layers

hbn = HexLattice('h-BN', dim = (100, 60))
hbn.write_lammps('../simulations/h-BN/lv_conductivity/test_pot/atoms.dat')

double_hbn = add_layers(hbn)
double_hbn.write_lammps('../simulations/h-BN/lv_conductivity/test_double_pot/atoms.dat')
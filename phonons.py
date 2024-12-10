# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from lattice import HexLattice

# create and plot
for angle in [0.91, 1.02, 1.05, 1.08, 1.12, 1.2, 1.35, 1.54]:
    graphene = HexLattice('LJ-graphene', dim = (1, 1), angle = angle)
    graphene.remove_overlapping_atoms()
    graphene.write_lammps(f'../data/phonons/TBG {angle}.dat')
    # print(graphene)
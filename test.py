# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from lattice import HexLattice, add_layers

lt = HexLattice('graphene', dim = (2, 2), angle = 5)
# lt.remove_overlapping_atoms()
print(lt)

lt.plot()
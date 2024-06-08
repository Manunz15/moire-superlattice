# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from lattice import HexLattice, add_layers

lt = HexLattice('graphene', dim = (2, 2), angle = 5)
# hbn.centering()
print(lt)

lt.plot()
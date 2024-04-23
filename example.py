# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from lattice import HexLattice, add_layers

# dim and angle
dim: tuple = (195, 100)
angle: float = 1.1

# create and plot
graphene = HexLattice('graphene', dim = dim)
double_graphene = add_layers(graphene, angle = angle)
double_graphene.plot()
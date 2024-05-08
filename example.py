# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from lattice import HexLattice, add_layers

# dim and angle
dim: tuple = (12, 20)
angle: float = 13.173551107258925

# create and plot
graphene = HexLattice('graphene', dim = dim)
double_graphene = add_layers(graphene, angle = angle)
double_graphene.plot()
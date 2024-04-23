from lattice import HexLattice, add_layers

# dim and angle
dim: tuple = (195, 100)
angle: float = 5

# create and plot
graphene = HexLattice('graphene', dim = dim)
# double_graphene = add_layers(graphene, angle = angle)
graphene.plot()
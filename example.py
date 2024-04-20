from create.hex import HexLattice
from create.second_layer import add_second_layer
from data.plot import PlotCrystal
from utils.materials import lattices

# define lattice
lattice = 'graphene'
step: float = lattices[lattice]['step']
z_step: float = lattices[lattice]['z_step']

# dim and angle
dim: tuple = (12, 20)
angle: float = 5

# create and plot
DF = HexLattice().create(step = step, dim = dim, atom_types = 1)
DF = add_second_layer(DF, angle = angle, trasl = [0, 0, z_step])
PlotCrystal(DF)
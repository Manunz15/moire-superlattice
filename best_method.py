from initialization.create_hex import HexLattice
from initialization.create_box import create_box
from initialization.add_second_layer import add_second_layer

from analysis.plot_crystal import PlotCrystal

import numpy as np

graphene_step = 1.42
elements = {'C': {'id': 1, 'mass': 12.011}}
square_width, height = 12, 21

# methods
ANGLES = np.concatenate((np.arange(0, 2, 0.1), np.arange(2, 10), np.arange(10, 50, 5)))
SHAPES = [(width, height) for width in range(square_width, height)]

for shape in SHAPES:
    hex_DF = HexLattice().create(step = graphene_step, dim = shape)

    for angle in ANGLES:
        DF = add_second_layer(hex_DF, angle = angle, trasl = [0, 0, 3.3])

        # box = create_box(hex_DF, delta = [graphene_step, graphene_step, 1000])
        box = create_box(DF, delta = [2, 2, 1000])
        PlotCrystal().plot_2d([DF], angle = round(angle, 1))
# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

import numpy as np
import pandas as pd

from initialization.transform import Transform

'''
ADD SECOND LAYER
----------------
Angle must be in degrees
'''

def add_second_layer(FIRST_LAYER: pd.DataFrame, angle: int, trasl: list[float]) -> pd.DataFrame:
    # create second layer
    FIRST_LAYER = Transform().rotation(FIRST_LAYER, angle = - angle / 2)
    SECOND_LAYER = Transform().rotation(FIRST_LAYER, angle = angle)
    SECOND_LAYER = Transform().translation(SECOND_LAYER, trasl = np.array(trasl))
    
    # concatenate layers
    SECOND_LAYER['id'] += len(FIRST_LAYER)
    TWO_LAYERS = pd.concat([FIRST_LAYER, SECOND_LAYER], ignore_index = True)

    return TWO_LAYERS
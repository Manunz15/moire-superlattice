# Lorenzo Manunza, Università degli Studi di Cagliari, March 2024

import pandas as pd

def create_box(DF: pd.DataFrame, delta: list[float] = ['0', '0', '0']) -> list[tuple]:
    """
    CREATE BOX
    -------------------------------------------------------------------------
    This function is used to create boxes for LAMMPS simulations.

    The box is created such that:
    1. It contains all the atoms contained in the 'DF' pandas dataframe;
    2. Its edges are parallel to the x,y,z axes;
    3. Its volume is minimized with the above two points satisfied.

    Its faces can be expanded thanks to a 'delta' list (default = [0, 0, 0]).
    Where the first element 'delta[0]' adds 'delta[0] / 2' units on the left 
    and 'delta[0] / 2' units on the right of the x-dimension of the box. The 
    same is true between the second (third) element and the y(z)-dimension.

    For example if the box initially spans from 0 to 5 in the x-axis and delta[0] 
    is 10,then the new box x-dimension will span from -5 to 10.
    """

    xlo, xhi = DF['x'].min() - delta[0] / 2, DF['x'].max() + delta[0] / 2
    ylo, yhi = DF['y'].min() - delta[1] / 2, DF['y'].max() + delta[1] / 2
    zlo, zhi = DF['z'].min() - delta[2] / 2, DF['z'].max() + delta[2] / 2

    return [(xlo, xhi), (ylo, yhi), (zlo, zhi)]
# Lorenzo Manunza, Università degli Studi di Cagliari, March 2024

import pandas as pd
import matplotlib.pyplot as plt
import inflect

"""
PLOT CRYSTAL
-------------------------------------------------------------------------
This class plots the crystal's atoms.

The atoms' positions must be stored in a list of pandas dataframe.

The graphs display:
1. The number of atoms as title
2. Different colors to different types of atoms
"""

class PlotCrystal:
    def __init__(self):
        # for ordinal numbers: 1 -> 1st
        self.p = inflect.engine()

    def plot(self, DFs: list[pd.DataFrame], ax, angle: float):
        # number of plotted atoms 
        num_atoms = 0

        for index, DF in enumerate(DFs):
            num_atoms += len(DF)

            # types of atoms
            for atom_type in DF['type'].unique():

                small_DF = DF.where(DF['type'] == atom_type).dropna()

                # labels
                if len(DFs) == 1:
                    label = f'{atom_type}'
                else:
                    label = f'{atom_type} - {self.p.ordinal(index + 1)} dataframe'

                # plot 2d
                if ax == plt:
                    ax.scatter(small_DF['x'], small_DF['y'], marker = '.', label = label)

                # plot 3d
                else:
                    ax.scatter(small_DF['x'], small_DF['y'], small_DF['z'], marker = '.', label = label)

        ax.axis('equal')

        title = f'{num_atoms} atoms - {angle}°' if angle != None else f'{num_atoms} atoms'
        plt.title(title)
        plt.legend(title = 'Types')
        plt.show()

    def plot_2d(self, DFs: list[pd.DataFrame], angle: float = None):
        self.plot(DFs = DFs, ax = plt, angle = angle)

    def plot_3d(self, DFs: list[pd.DataFrame]):
        fig = plt.figure()
        ax = fig.add_subplot(projection = '3d')
        self.plot(DFs = DFs, ax = ax)
# Lorenzo Manunza, Università degli Studi di Cagliari, March 2024

import pandas as pd
import matplotlib.pyplot as plt

"""
PLOT CRYSTAL
-------------------------------------------------------------------------
This class plots the crystal's atoms.

The atoms' positions must be stored in a list of pandas dataframe.

The graphs display:
1. The number of atoms as title
2. Different colors to different types of atoms
"""

class AtomsPlot:
    def __init__(self, atoms: pd.DataFrame, name: str = None, projection: str = '2d') -> None:
        # initialization
        self.color = {1: '#009bff', 2: '#ff0000', 3: '#2ae700'}

        # plot
        if projection == '2d':
            self.plot_2d(atoms = atoms, name = name)
        elif projection == '3d':
            self.plot_3d(atoms = atoms, name = name)
        else:
            raise Warning(f"<projection> must be '2d' or '3d', not '{projection}'.")

    def plot_2d(self, atoms: pd.DataFrame, name: str) -> None:
        self.plot(atoms = atoms, ax = plt, name = name)

    def plot_3d(self, atoms: pd.DataFrame, name: str) -> None:
        fig = plt.figure()
        ax = fig.add_subplot(projection = '3d')
        self.plot(atoms = atoms, ax = ax, name = name)

    def plot(self, atoms: pd.DataFrame, name: str, ax: plt) -> None:
        # number of plotted atoms 
        num_atoms = len(atoms)

        # types of atoms
        for atom_type in atoms['type'].unique():
            label = f'{atom_type}'
            fewer_atoms = atoms.where(atoms['type'] == atom_type).dropna()

            # plot 2d
            if ax == plt:
                ax.scatter(fewer_atoms['x'], fewer_atoms['y'], marker = '.', label = label, c = self.color[int(atom_type)])

            # plot 3d
            else:
                ax.scatter(fewer_atoms['x'], fewer_atoms['y'], fewer_atoms['z'], marker = '.', label = label, c = self.color[int(atom_type)])

        ax.axis('equal')
        title = f'{name} - {num_atoms} atoms' if name else f'{num_atoms} atoms'
        plt.title(title)
        plt.legend(title = 'Atom types')
        plt.show()
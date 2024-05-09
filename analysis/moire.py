# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis.extrapolated import ExtrConductivity

import os
import matplotlib.pyplot as plt
from tqdm import tqdm

class MoireConductivity:
    def __init__(self, path: str, lattice: str) -> None:
        # initialization
        self.path: str = path
        self.lattice: str = lattice

        self.k_list: list[float] = []
        self.angle_list: list[float] = []
        self.exco_list: list[ExtrConductivity] = []

        self.read_data()

    def read_data(self) -> None:
        for dir in tqdm(os.listdir(self.path), ascii = ' =', bar_format = '{l_bar}{bar:50}{r_bar}{bar:-10b}'):
            angle = float(dir.split('_')[-1])
            new_path = os.path.join(self.path, dir)
            exco = ExtrConductivity(new_path, self.lattice, 2)

            self.k_list.append(exco.k)
            self.angle_list.append(angle)
            self.exco_list.append(exco)

    def plot(self) -> None:
        plt.plot(self.angle_list, self.k_list, marker = '.')
        plt.xlabel(f'$\\theta$°')
        plt.ylabel(f'k[2/K$\cdot$m]')
        plt.show()
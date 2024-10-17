# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis.extrapolated import ExtrConductivity
from lattice.hex import HexLattice as hex

import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

class MoireConductivity:
    def __init__(self, path: str, lattice: str, num_layers: int = 2, plot: bool = False) -> None:
        # initialization
        self.path: str = path
        self.lattice: str = lattice
        self.num_layers: int = num_layers

        self.k_list: list[float] = []
        self.err_list: list[float] = []
        self.angle_list: list[float] = []
        self.exco_list: list[ExtrConductivity] = []

        self.read_data(plot)

    def read_data(self, plot: bool) -> None:
        for dir in tqdm(os.listdir(self.path), ascii = ' =', bar_format = '{l_bar}{bar:50}{r_bar}{bar:-10b}'):
            angle = float(dir.split('_')[-1])
            new_path = os.path.join(self.path, dir)
            exco = ExtrConductivity(new_path, self.lattice, self.num_layers)

            if angle:
                _, __, angle = hex.moire_angle(angle)
            
            self.k_list.append(exco.k)
            self.err_list.append(exco.k_err)
            self.angle_list.append(round(angle, 2))
            self.exco_list.append(exco)

            if plot:
                exco.plot()

    def plot(self, err = False) -> None:    
        if err:
            plt.errorbar(self.angle_list, self.k_list, yerr = self.err_list, marker = 'o')
        else:
            plt.plot(self.angle_list, self.k_list, marker = 'o')
        plt.xlabel(r'$\theta$°')
        plt.ylabel(r'k[W/K$\cdot$m]')
        plt.show()

    def save(self, filename: str) -> None:
        DF = pd.DataFrame({'angles': self.angle_list, 'k': self.k_list, 'k_err': self.err_list})
        DF.to_csv(f'{filename}.csv')
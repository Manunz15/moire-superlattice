# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis.extrapolated import ExtrConductivity
from lattice.hex import HexLattice as hex

import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

class MoireConductivity:
    def __init__(self, paths: list[str], lattice: str, num_layers: int = 2, plot: bool = False) -> None:
        # initialization
        self.paths: list[str] = paths if type(paths) == list else [paths]
        self.lattice: str = lattice
        self.num_layers: int = num_layers

        # find paths
        self.dict: dict[float, list[str]] = {}
        self.find_paths()

        self.k_list: list[float] = []
        self.err_list: list[float] = []
        self.angle_list: list[float] = []
        self.exco_list: list[ExtrConductivity] = []

        self.read_data(plot)

    def find_paths(self) -> None:
        for path in self.paths:
            for dir in os.listdir(path):
                angle = float(dir.split('_')[-1])
                _, __, angle = hex.moire_angle(angle)
                angle = round(angle, 2)

                new_path = os.path.join(path, dir)

                if angle in self.dict.keys():
                    self.dict[angle].append(new_path)
                else:
                    self.dict[angle] = [new_path]

    def read_data(self, plot: bool) -> None:
        for angle, paths in tqdm(self.dict.items(), ascii = ' =', bar_format = '{l_bar}{bar:50}{r_bar}{bar:-10b}'):
            exco = ExtrConductivity(paths, self.lattice, self.num_layers)
            
            self.k_list.append(exco.k)
            self.err_list.append(exco.k_err)
            self.angle_list.append(angle)
            self.exco_list.append(exco)

            if plot:
                exco.plot()

    def plot(self, err = True, hold = False) -> None:    
        if err:
            plt.errorbar(self.angle_list, self.k_list, yerr = self.err_list, marker = 'o')
        else:
            plt.plot(self.angle_list, self.k_list, marker = 'o')
        plt.xlabel(r'$\theta$°')
        plt.ylabel(r'k[W/K$\cdot$m]')

        if not hold:
            plt.show()

    def save(self, filename: str) -> None:
        DF = pd.DataFrame({'angles': self.angle_list, 'k': self.k_list, 'k_err': self.err_list})
        DF.to_csv(f'{filename}.csv')
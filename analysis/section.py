# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis.lampin import Lampin

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Section:
    def __init__(self, path: str, lattice: str, num_layers: int = 2) -> None:
        # initialization
        self.path: str = path
        self.lattice: str = lattice
        self.num_layers: int = num_layers

        self.k_list: list[float] = []
        self.err_list: list[float] = []
        self.S_list: list[float] = []
        self.lampin_list: list[Lampin] = []

        self.read_data()
        self.average()
    
    def read_data(self) -> None:
        for dir in os.listdir(self.path):
            new_path = os.path.join(self.path, dir)
            lp = Lampin(new_path, self.lattice, self.num_layers)

            self.k_list.append(lp.k)
            self.err_list.append(lp.k_err)
            self.S_list.append(lp.S / 100)  # from angstrom^2 to nm^2
            self.lampin_list.append(lp)

    def average(self) -> None:
        self.k_ave: float = np.mean(self.k_list)
        self.rms: float = np.sqrt(np.sum((np.array(self.k_list) - self.k_ave)**2) / (len(self.k_list) - 1))
        self.sdom: float = self.rms / np.sqrt(len(self.k_list))
        self.k_ave_err: float = self.rms / np.sqrt(len(self.k_list))
        self.ave_rms_perc: float = 100 * self.rms / self.k_ave

    def plot(self) -> None:
        X_ave: list[float] = [0.8 * min(self.S_list), 1.05 * max(self.S_list)]
        y_ave: list[float] = [self.k_ave] * 2

        plt.errorbar(self.S_list, self.k_list, yerr = self.rms, marker = 'o', zorder = 0, label = rf'RMS = {self.rms:.0f}W/K$\cdot$m ({self.ave_rms_perc:.1f}% of average)')
        plt.plot(X_ave, y_ave, '--', c = 'r', label = rf'$k_{{ave}}$ = ({self.k_ave:.1f}$\pm${self.k_ave_err:.1f})W/K$\cdot$m')
        plt.xlabel(r'S[nm$^{2}$]')
        plt.ylabel(r'k[W/K$\cdot$m]')
        plt.legend()
        plt.show()

    def save(self, filename: str):
        DF = pd.DataFrame({
            'S': self.S_list,
            'k': self.k_list,
        })
                
        ave_DF = pd.DataFrame({
            'k_ave': [self.k_ave],
            'rms': [self.rms],
            'sdom': [self.sdom],
        })

        DF.to_csv(f'{filename}.csv')
        ave_DF.to_csv(f'{filename}_ave.csv')
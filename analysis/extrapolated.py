# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis.lampin import Lampin

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

class ExtrConductivity:
    def __init__(self, path: str, lattice: str, num_layers: int = 1, plot: bool = False) -> None:
        # initialization
        self.path: str = path
        self.lattice: str = lattice
        self.num_layers: int = num_layers

        self.k: float = 0
        self.inv_k_list: list[float] = []
        self.inv_L_list: list[float] = []
        self.lampin_list: list[Lampin] = []

        self.read_data()
        self.extract_conductivity(plot)

    def __str__(self) -> str:
        return f'k = {self.k:.3f}'
    
    def read_data(self) -> None:
        for dir in os.listdir(self.path):
            new_path = os.path.join(self.path, dir)
            lp = Lampin(new_path, self.lattice, self.num_layers)

            self.inv_k_list.append(1 / lp.k)
            self.inv_L_list.append(1 / lp.L)
            self.lampin_list.append(lp)

    def polynomial(self, X: np.array, a: float, b: float, c: float) -> float:
        return a * X**2 + b * X + c
    
    def extract_conductivity(self, plot: bool = False) -> None:
        pars, _ = curve_fit(f = self.polynomial, xdata = self.inv_L_list, ydata = self.inv_k_list)
        self.k = 1 / pars[-1]

        if plot:
            X_fit = np.linspace(0, max(self.inv_L_list) * 1.2, 100)
            y_fit = self.polynomial(X_fit, * pars)

            plt.plot(X_fit, y_fit, '--', c = 'r', label = rf'$k_\infty$ = {self.k:.3f} W/K$\cdot$m')
            plt.legend()
            self.plot()

    def plot(self) -> None:
        plt.scatter(self.inv_L_list, self.inv_k_list, zorder = 0)
        plt.xlabel(r'1/L[$\AA^{-1}$]')
        plt.ylabel(r'1/k[K$\cdot$m/W]')
        plt.show()
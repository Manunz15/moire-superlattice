# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis.lampin import Lampin
from analysis.printable import Printable

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

class ExtrConductivity(Printable):
    def __init__(self, path: str, lattice: str, num_layers: int = 1, plot: bool = False) -> None:
        super().__init__()

        # initialization
        self.path: str = path
        self.lattice: str = lattice
        self.num_layers: int = num_layers

        self.k: float = 0
        self.inv_k_list: list[float] = []
        self.inv_err_list: list[float] = []
        self.inv_L_list: list[float] = []
        self.lampin_list: list[Lampin] = []

        self.read_data(plot)
        self.extract_conductivity()
    
    def read_data(self, plot: bool) -> None:
        for dir in os.listdir(self.path):
            new_path = os.path.join(self.path, dir)
            lp = Lampin(new_path, self.lattice, self.num_layers)
            lp.plot()

            self.inv_k_list.append(1 / lp.k)
            self.inv_err_list.append(lp.k_err / lp.k ** 2)
            self.inv_L_list.append(1 / lp.L)
            self.lampin_list.append(lp)

            if plot:
                lp.plot()

    def polynomial(self, X: np.array, a: float, b: float, c: float) -> float:
        return a * X**2 + b * X + c
    
    def extract_conductivity(self) -> None:
        pars, covs = curve_fit(f = self.polynomial, xdata = self.inv_L_list, ydata = self.inv_k_list, sigma = self.inv_err_list)
        self.k = 1 / pars[-1]
        self.k_err = np.sqrt(covs[-1][-1]) / pars[-1]**2

        self.X_fit = np.linspace(0, max(self.inv_L_list) * 1.2, 100)
        self.y_fit = self.polynomial(self.X_fit, * pars)

    def plot(self) -> None:
        plt.errorbar(self.inv_L_list, self.inv_k_list, yerr = self.inv_err_list, fmt="o", zorder = 0)
        plt.plot(self.X_fit, self.y_fit, '--', c = 'r', label = rf'$k_\infty$ = ({self.k:.0f}$\pm${self.k_err:.0f})W/K$\cdot$m')
        plt.xlabel(r'1/L[$\AA^{-1}$]')
        plt.ylabel(r'1/k[K$\cdot$m/W]')
        plt.legend()
        plt.show()
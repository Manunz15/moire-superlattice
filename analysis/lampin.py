# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis.read import read_log, read_box
from lattice.presets import lattices
from utils.settings import K_B

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from typing import Callable

class Lampin:
    def __init__(self, path: str, lattice: str, num_layers: int = 2) -> None:
        # initialization
        self.path: str = path
        self.lattice: str = lattice
        self.num_layers: int = num_layers
        self.z_step = lattices[lattice]['z_step']

        self.k: float = 0
        self.k_list: list[float] = []
        self.chi2_list: list[float] = []
        self.rchi2_list: list[float] = []

        self.read_data()
        self.conductivity_trend()

    def __str__(self) -> str:
        return f'k = {self.k:.3f}W/K$\cdot$m'

    def read_data(self) -> None:
        # read data
        log_file: str = os.path.join(self.path, 'log.lammps')
        nve_file: str = os.path.join(self.path, 'log.nve')
        data: pd.DataFrame = read_log(nve_file)

        # values
        self.num_atoms: int = data['Atoms'][0]
        box: list[tuple[float]] = read_box(log_file)
        self.L = box[0][1] - box[0][0]                                              # angstrom
        self.S: float = box[1][1] - box[1][0] * self.z_step * self.num_layers       # angstrom^2

        # select data
        time: np.array = data['Step'].to_numpy() * 1e-15
        self.X: np.array = (time - time.min())
        self.y: np.array = data['v_deltaT'].to_numpy()

    def sum_exp(self, n: int = 1) -> Callable:
        def curve(X: np.array, a: float, tau: float) -> float:
            func: int = 0
            for m in range(n):
                k: int = (2 * m + 1)**2
                func += a * np.exp(- k * X / tau) / k
            return func
        return curve
    
    def k_exp(self, X: np.array, a: float, b: float) -> float:
        return a * (1 - np.exp(- X / b))
        
    def find_conductivity(self, threshold: float = 1, plot: bool = False) -> None:
        # data
        exp_series = self.sum_exp(5)
        X: np.array = self.X[:int(len(self.X) * threshold)]
        y: np.array = self.y[:int(len(self.y) * threshold)]

        # fitting
        pars, _ = curve_fit(f = exp_series, xdata = X, ydata = y, p0 = [y[0], self.X[np.where(y > y[0] / np.e)][-1]])

        # thermal conductivity
        k: float = ((3 * K_B) * self.L * self.num_atoms) / (4 * (np.pi ** 2) * (pars[1] * 1) * self.S) * 1e10

        # chi squared
        y_pred: np.array = exp_series(X, *pars)
        chi2: float = (np.linalg.norm(y - y_pred)**2) / y_pred.sum() 
        rchi2: float = chi2 / (len(X) - 2)

        # plot
        if plot:
            X_fit: np.array = np.linspace(0, X.max(), 101)
            y_fit: np.array = exp_series(X_fit, *pars)
            plt.plot(X_fit, y_fit, '--', c = 'r')
            self.plot(X, y)
        
        return k, chi2, rchi2

    def conductivity_trend(self, num_points: int = 40, plot: bool = False) -> None:
        self.thresholds = np.linspace(1 / num_points, 1, num_points)

        for threshold in self.thresholds:
            k, chi2, rchi2 = self.find_conductivity(threshold)
            self.k_list.append(k)
            self.chi2_list.append(chi2)
            self.rchi2_list.append(rchi2)

        pars, _ = curve_fit(f = self.k_exp, xdata = self.thresholds, ydata = np.array(self.k_list), 
                            p0 = [max(self.k_list), self.thresholds.max()])
        self.k = pars[0]
        
        if plot:
            y_fit: np.array = self.k_exp(self.thresholds, *pars)
            plt.plot(self.thresholds, y_fit, '--', c = 'r', label = f'$k_\infty$ = {self.k:.3f} W/K$\cdot$m')
            plt.legend()
            self.plot_trend()

    def plot(self, X: np.array = None, y: np.array = None) -> None:
        if X is None or y is None:
            X = self.X
            y = self.y

        plt.plot(X, y, zorder = 0)
        plt.xlabel('Time[s]')
        plt.ylabel('$\Delta$T[K]')
        plt.show()

    def plot_trend(self, value: str = 'k') -> None:
        # plottable values
        plottable_values: dict[str, dict] = {'k': {'data': self.k_list, 'label': 'k[W/K$\cdot$m]'}, 
                                            'chi2': {'data': self.chi2_list, 'label': '$\chi^2$'}, 
                                            'rchi2': {'data': self.rchi2_list, 'label': '$\\tilde{\chi}^2$'}}
        
        if value not in plottable_values.keys():
            raise NameError(f'{value} is not a plottable value. Choose between: {list(plottable_values.keys())}')
        
        plt.plot(self.thresholds, plottable_values[value]['data'], marker = '.', zorder = 0)
        plt.xlabel('Threshold')
        plt.ylabel(plottable_values[value]['label'])
        plt.show()
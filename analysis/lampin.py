# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis.read import read_log, read_box
from analysis.printable import Printable
from lattice.presets import lattices
from utils.settings import K_B

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from typing import Callable, Any

class Lampin(Printable):
    def __init__(self, path: str, lattice: str, num_layers: int = 2) -> None:
        super().__init__()
        
        # initialization
        self.path: str = path
        self.lattice: str = lattice
        self.num_layers: int = num_layers
        self.z_step = lattices[lattice]['z_step']

        self.k: float = 0
        self.k_list: list[float] = []
        self.err_list: list[float] = []
        self.chi2_list: list[float] = []
        self.rchi2_list: list[float] = []

        self.read_data()
        self.conductivity_trend()

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
        self.T: float = data['Temp'][len(data) - 1]

        # select data
        time: np.ndarray = data['Step'].to_numpy() * 1e-15
        self.X: np.ndarray = (time - time.min())
        self.y: np.ndarray = data['v_deltaT'].to_numpy()

    def sum_exp(self, n: int = 1) -> Callable:
        def curve(X: Any, a: float, tau: float) -> Any:
            func: int = 0
            for m in range(n):
                k: int = (2 * m + 1)**2
                func += a * np.exp(- k * X / tau) / k
            return func
        return curve
    
    def k_exp(self, X: Any, a: float, b: float) -> Any:
        return a * (1 - np.exp(- X / b))
        
    def find_conductivity(self, threshold: float = 1, plot: bool = False) -> None:
        # data
        exp_series = self.sum_exp(5)
        X: np.ndarray = self.X[:int(len(self.X) * threshold)]
        y: np.ndarray = self.y[:int(len(self.y) * threshold)]

        # fitting
        pars, covs = curve_fit(f = exp_series, xdata = X, ydata = y, p0 = [y[0], self.X[np.where(y > y[0] / np.e)][-1]])
        self.temp_fit: np.ndarray = exp_series(X, *pars)

        # thermal conductivity
        k: float = ((3 * K_B) * self.L * self.num_atoms) / (4 * (np.pi ** 2) * pars[1] * self.S) * 1e10
        k_err: float = k * (np.sqrt(covs[1][1]) / pars[1])

        # chi squared
        y_pred: np.array = exp_series(X, *pars)
        chi2: float = (np.linalg.norm(y - y_pred)**2) / y_pred.sum() 
        rchi2: float = chi2 / (len(X) - 2)

        # plot
        if plot:
            plt.plot(X, self.temp_fit, '--', c = 'r')
            self.plot_temp(X, y)
        
        return k, k_err, chi2, rchi2

    def conductivity_trend(self, num_points: int = 50, plot: bool = False) -> None:
        self.thresholds = np.linspace(0.01, 1, num_points)

        for threshold in self.thresholds:
            k, k_err, chi2, rchi2 = self.find_conductivity(threshold)
            self.k_list.append(k)
            self.err_list.append(k_err)
            self.chi2_list.append(chi2)
            self.rchi2_list.append(rchi2)

        # fit conductivity
        pars, covs = curve_fit(f = self.k_exp, xdata = self.thresholds, ydata = np.array(self.k_list), 
                            p0 = [self.k_list[-1], 1], sigma = self.err_list)

        self.k = pars[0]
        self.k_err = 0.05 * self.k  # from the study of section dependance
        self.y_fit: np.array = self.k_exp(self.thresholds, *pars)
        
        # plot
        if plot:
            self.plot()

    def plot_temp(self, X: np.array = None, y: np.array = None) -> None:
        if X is None or y is None:
            X = self.X
            y = self.y
            plt.plot(X, self.temp_fit, '--', c = 'r')

        plt.plot(X, y, zorder = 0)
        plt.xlabel('Time[s]')
        plt.ylabel(r'$\Delta$T[K]')
        plt.show()

    def plot(self, value: str = 'k') -> None:
        # plottable values
        plottable_values: dict[str, dict] = {'k': {'data': self.k_list, 'yerr': self.err_list, 'ylabel': r'k[W/K$\cdot$m]'}, 
                                            'chi2': {'data': self.chi2_list, 'yerr': None, 'ylabel': r'$\chi^2$'}, 
                                            'rchi2': {'data': self.rchi2_list, 'yerr': None, 'ylabel': r'$\tilde{\chi}^2$'}}
        
        if value not in plottable_values.keys():
            raise NameError(f'{value} is not a plottable value. Choose between: {list(plottable_values.keys())}')
        
        if value == 'k':
            plt.plot(self.thresholds, self.y_fit, '--', c = 'r', label = rf'$k_\infty$ = ({self.k:.3f}$\pm${self.k_err:.3f})W/K$\cdot$m')
            plt.legend()
        
        plt.errorbar(self.thresholds, plottable_values[value]['data'], yerr = plottable_values[value]['yerr'], marker = '.', zorder = 0)
        plt.xlabel('Threshold')
        plt.ylabel(plottable_values[value]['ylabel'])
        plt.show()

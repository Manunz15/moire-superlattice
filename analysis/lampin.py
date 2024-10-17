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
    def __init__(self, path: str, 
                 lattice: str, 
                 num_layers: int = 2, 
                 num_points: int = 25,
                 num_exp: int = 5, 
                 plot: bool = False, 
                 save_path: str | None = None) -> None:
        super().__init__()
        
        # initialization
        self.path: str = path
        self.lattice: str = lattice
        self.num_layers: int = num_layers
        self.z_step = lattices[lattice]['z_step_after']
        self.err_perc = lattices[lattice]['err']
        self.num_exp = num_exp
        self.save_path = save_path

        self.k: float = 0
        self.k_list: list[float] = []
        self.err_list: list[float] = []
        self.chi2_list: list[float] = []
        self.rchi2_list: list[float] = []

        self.read_data()
        self.conductivity_trend(num_points, plot)

    def read_data(self) -> None:
        # read data
        final_file: str = os.path.join(self.path, 'final.atoms')
        nve_file: str = os.path.join(self.path, 'log.nve')
        data: pd.DataFrame = read_log(nve_file)

        # values
        self.num_atoms: int = data['Atoms'][0]
        box: list[tuple[float]] = read_box(final_file)
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
        
    def find_conductivity(self, threshold: float = 1, plot: bool = False, save: bool = False) -> None:
        # data
        exp_series = self.sum_exp(self.num_exp)
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

        if self.save_path:
            self.save_temp(X, y, pars, covs)
        
        return k, k_err, chi2, rchi2

    def conductivity_trend(self, num_points: int, plot: bool) -> None:
        self.thresholds = np.linspace(0.04, 1, num_points)
        # self.thresholds = [0.04, 0.08, 0.12, 0.2, 0.4, 1]

        for threshold in self.thresholds:
            k, k_err, chi2, rchi2 = self.find_conductivity(threshold, plot)
            self.k_list.append(k)
            self.err_list.append(k_err)
            self.chi2_list.append(chi2)
            self.rchi2_list.append(rchi2)

        # fit conductivity
        pars, covs = curve_fit(f = self.k_exp, xdata = self.thresholds, ydata = np.array(self.k_list), 
                            p0 = [self.k_list[-1], 1], sigma = self.err_list)

        self.pars = pars
        self.covs = covs
        self.k = pars[0]
        self.k_err = self.err_perc * self.k  # from the study of section dependance
        self.y_fit: np.array = self.k_exp(self.thresholds, *pars)

        # print(f'{self.num_exp} -> k = {self.k:.2f} +- {np.sqrt(covs[0][0]):.2f}')

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

    def save_temp(self, X: np.ndarray, y: np.ndarray, pars: list[float], covs: list[float]):
        i = next_num()

        # data
        DF = pd.DataFrame({'X': X, 'y': y})
        DF.to_csv(f'{self.save_path}/{i}.csv')

        # fit data
        fit_DF = pd.DataFrame({'dT': [pars[0]], 'dT_err': [np.sqrt(covs[0][0])], 
                               'tau': [pars[1]], 'tau_err': [np.sqrt(covs[1][1])], 
                               'num_exp': [self.num_exp]})
        fit_DF.to_csv(f'{self.save_path}/fit_{i}.csv')
        
    def save(self, filename: str):
        # data
        DF = pd.DataFrame({'X': self.thresholds, 'y': self.k_list, 'y_err': self.err_list})
        DF.to_csv(f'{filename}.csv')

        # fit data
        fit_DF = pd.DataFrame({'a': [self.pars[0]], 'a_err': [np.sqrt(self.covs[0][0])], 
                               'b': [self.pars[1]], 'b_err': [np.sqrt(self.covs[1][1])]})
        fit_DF.to_csv(f'{filename}_fit.csv')

num = 0
def next_num():
    global num
    num += 1
    return num
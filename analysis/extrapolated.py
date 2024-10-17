# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis.lampin import Lampin
from analysis.printable import Printable

from sklearn import linear_model
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import argrelmin

class ExtrConductivity(Printable):
    def __init__(self, path: str, lattice: str, num_layers: int = 2, plot: bool = False) -> None:
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

            self.inv_k_list.append(1 / lp.k)
            self.inv_err_list.append(lp.k_err / lp.k ** 2)
            self.inv_L_list.append(10 / lp.L)               # from angstrom to nm
            self.lampin_list.append(lp)

            if plot:
                lp.plot()

    def linear(self, X: np.array, a: float, b: float) -> float:
        return a * X + b
    
    def polynomial(self, X: np.array, a: float, b: float, c: float) -> float:
        return a * X**2 + b * X + c
    
    def lasso(self, X: list[float], y: list[float], yerr: list[float]):
        # data
        X: np.ndarray = np.array(X)
        X2: np.ndarray = X ** 2
        y: np.ndarray = np.array(y)

        new_X = np.zeros([len(X), 2])
        new_X[:,0] = (X - X.mean()) / X.std()
        new_X[:,1] = (X2 - X2.mean()) / X2.std()
        new_y = (y - y.mean()) / y.std()

        # study of alpha
        self.alphas = np.logspace(-10, 1, 100)
        self.coef1_list = []
        self.coef2_list = []
        for alpha in self.alphas:
            lasso = linear_model.Lasso(alpha = alpha)
            lasso.fit(new_X, new_y, sample_weight = yerr)
            
            # save
            self.coef1_list.append(lasso.coef_[0])
            self.coef2_list.append(lasso.coef_[1])

        zero1 = np.where(np.array(self.coef1_list) == 0)[0][0]
        zero2 = np.where(np.array(self.coef2_list) == 0)[0][0]

        return zero2 > zero1

    def extract_conductivity(self) -> None:
        # lasso regression check
        self.second_order: bool = self.lasso(X = self.inv_L_list, y = self.inv_k_list, yerr = self.inv_err_list)
        if self.second_order:
            fit_curve = self.polynomial
        else:
            fit_curve = self.linear

        # fitting
        pars, covs = curve_fit(f = fit_curve, xdata = self.inv_L_list, ydata = self.inv_k_list, sigma = self.inv_err_list)
        self.pars = pars
        self.covs = covs
        self.k = 1 / pars[-1]
        self.k_err = np.sqrt(covs[-1][-1]) / pars[-1]**2

        self.X_fit = np.linspace(0, max(self.inv_L_list) * 1.2, 100)
        self.y_fit = fit_curve(self.X_fit, * pars)

    def plot(self) -> None:
        order = 2 if self.second_order else 1

        plt.errorbar(self.inv_L_list, self.inv_k_list, yerr = self.inv_err_list, fmt="o", zorder = 0)
        plt.plot(self.X_fit, self.y_fit, '--', c = 'r', label = rf'$k_\infty^{{({order})}}$ = ({self.k:.0f}$\pm${self.k_err:.0f})W/K$\cdot$m')
        plt.xlabel(r'1/L[nm$^{-1}$]')
        plt.ylabel(r'1/k[K$\cdot$m/W]')
        plt.legend()
        plt.show()
        
    def plot_lasso(self) -> None:
        plt.plot(self.alphas, self.coef1_list, label = 'coef 1')
        plt.plot(self.alphas, self.coef2_list, label = 'coef 2')
        plt.legend()
        plt.xscale('log')
        plt.show()

    def save(self, filename: str, only_k: bool = False) -> None:
        # k data
        k_DF = pd.DataFrame({'k': [self.k], 'k_err': [self.k_err], 
                               'order': [int(self.second_order) + 1]})
        k_DF.to_csv(f'{filename}_k.csv')

        if not only_k:
            # data
            DF = pd.DataFrame({'X': self.inv_L_list, 'y': self.inv_k_list, 'y_err': self.inv_err_list})
            DF.to_csv(f'{filename}.csv')

            # fit data
            fit_DF = pd.DataFrame({'pars': self.pars, 'err': np.sqrt(np.diag(self.covs))})
            fit_DF.to_csv(f'{filename}_fit.csv')

            # lasso data
            lasso_DF = pd.DataFrame({'alpha': self.alphas, 'coef1': self.coef1_list, 'coef2': self.coef2_list})
            lasso_DF.to_csv(f'{filename}_lasso.csv')
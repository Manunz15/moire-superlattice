# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from analysis.read import read_log, read_box
from analysis.find_conductivity import find_conductivity
from analysis.plot import plot_fit, plot_extracted
from scipy.optimize import curve_fit

import os
import numpy as np

def taylor(X, a, b, c):
    return a * X**2 + b * X + c

def extract_conductivity(path: str, threshold: float = 0.5, p0 = [1, 1], num_layers: int = 2, plot: bool = False):
    # read data
    log_file = os.path.join(path, 'log.lammps')
    nve_file = os.path.join(path, 'log.nve')
    data = read_log(nve_file)
    box = read_box(log_file)

    # data
    # n = data.index[data['v_deltaT'] < threshold * data['v_deltaT'].max()].to_numpy()[0]
    # time = data['Step'][:n] * 1e-15
    # dT = data['v_deltaT'][:n]
    time = data['Step'][:int(len(data) * threshold)] * 1e-15
    dT = data['v_deltaT'][:int(len(data) * threshold)]
    time = (time - time.min())

    # values
    atoms_num: int = data['Atoms'][0]
    L: float = box[0][1] - box[0][0]
    S: float = box[1][1] - box[1][0] * 3.3 * num_layers

    # fit
    k, red_chi2, pars, covs, time_fit, dT_fit = find_conductivity(time, dT, atoms_num, L, S, p0 = p0)

    # plot
    if plot:
        plot_fit(time, dT, time_fit, dT_fit)

    return k, red_chi2, L

def ultimate_conductivity(path: str, threshold: float = 0.5, p0 = [1, 1], num_layers: int = 2, plot_final: bool = False, plot_every: bool = False) -> float:
    # initialization
    k_list: list[float] = []
    L_list: list[float] = []
    chi2_list: list[float] = []

    for dir in os.listdir(path):
        # read data and fit
        new_path = os.path.join(path, dir)
        k, chi2, L = extract_conductivity(path = new_path, threshold = threshold, p0 = p0, num_layers = num_layers, plot = plot_every)

        # save data
        k_list.append(k)
        L_list.append(L)
        chi2_list.append(chi2)
    
    # extract thermal conductivity
    inverted_k = 1 / np.array(k_list)
    inverted_L = 1 / np.array(L_list)

    pars, _ = curve_fit(f = taylor, xdata = inverted_L, ydata = inverted_k)
    X_fit = np.linspace(0, inverted_L.max(), 3)
    y_fit = taylor(X_fit, * pars)

    k_inf = 1 / taylor(0, * pars)
    av_chi2 = sum(chi2_list) / len(chi2_list)

    # plot
    if plot_final or plot_every:
        plot_extracted(inverted_k, inverted_L, X_fit, y_fit, k_inf)

    return k_inf, av_chi2

# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from typing import Any

from utils.settings import K_B

def sum_exp(n: int = 1) -> Any:
    def curve(X, a, tau) -> float:
        func = 0
        for m in range(n):
            k = (2 * m + 1)**2
            func += a * np.exp(- k * X / tau) / k
        return func
    
    return curve

def find_conductivity(time: pd.Series, dT: pd.Series, atoms_num: int, L: float, S: float, p0: list[float]) -> Any:
    # fitting
    func = sum_exp(5)
    pars, covs = curve_fit(f = func, xdata = time, ydata = dT, p0 = p0)
    time_fit = np.linspace(0, time.max(), 101)
    dT_fit = func(time_fit, * pars)

    # thermal conductivity
    k = ((3 * K_B) * L * atoms_num) / (4 * (np.pi ** 2) * (pars[1] * 1) * S) * 1e10

    # chi squared
    dT: np.array = dT.to_numpy()
    dT_pred: np.array = func(time, *pars).to_numpy()
    reduced_chi2: float = (np.linalg.norm(dT - dT_pred)**2) / (dT_pred.sum() * (len(time) - 2))
    
    return k, reduced_chi2, pars, covs, time_fit, dT_fit
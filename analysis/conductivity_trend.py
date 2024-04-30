# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from analysis.read import read_log
from analysis.find_conductivity import find_conductivity
from analysis.plot import plot_fit, plot_extracted
from scipy.optimize import curve_fit

import os
import numpy as np

def rect(X, a, b):
    return a * X + b

def extract_conductivity(path: str, threshold: float = 0.6, p0 = [1, 1], plot_final: bool = False, plot_every: bool = False) -> float:
    # initialization
    k_list: list[float] = []
    L_list: list[float] = []
    chi2_list: list[float] = []

    for file in os.listdir(path):
        # read data
        filename = '/'.join([path, file])
        data = read_log(filename)

        # data
        n = data.index[data['v_deltaT'] > threshold * data['v_deltaT'].max()].to_numpy()[-1]
        time = data['Step'][:n] * 1e-15
        dT = data['v_deltaT'][:n]
        time = (time - time.min())

        # values
        dim = tuple(map(int, filename[-7:].replace('_', '').split(sep = 'x')))
        atoms_num: int = data['Atoms'][0]
        L: float = dim[0] * 1.42 * 2 * (1 + np.cos(np.pi / 3))
        S: float = dim[1] * 1.42 * 2 * np.sin(np.pi / 3) * 3.3

        # fit
        k, chi2, pars, covs, time_fit, dT_fit = find_conductivity(time, dT, atoms_num, L, S, p0 = p0)

        # save data
        k_list.append(k)
        L_list.append(L)
        chi2_list.append(chi2)

        # plot
        if plot_every:
            plot_fit(time, dT, time_fit, dT_fit)
    
    # extract thermal conductivity
    inverted_k = 1 / np.array(k_list)
    inverted_L = 1 / np.array(L_list)

    pars, _ = curve_fit(f = rect, xdata = inverted_L, ydata = inverted_k)
    X_fit = np.linspace(0, inverted_L.max(), 3)
    y_fit = rect(X_fit, * pars)

    k_inf = 1 / rect(0, * pars)
    av_chi2 = sum(chi2_list) / len(chi2_list)

    # plot
    if plot_final or plot_every:
        plot_extracted(inverted_k, inverted_L, X_fit, y_fit, k_inf)

    return k_inf, av_chi2
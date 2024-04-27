# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from typing import Any
import os

from analysis.setting import K_B

def sum_exp(n: int = 1) -> Any:
    def curve(X, a, tau):
        func = 0
        for m in range(n):
            k = (2 * m + 1)**2
            func += a * np.exp(- k * X / tau) / k
        return func
    
    return curve

def find_conductivity(time: pd.Series, dT: pd.Series, atoms_num: int, L: float, S: float, p0: list[float]) -> Any:
    # fitting
    func = sum_exp()
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
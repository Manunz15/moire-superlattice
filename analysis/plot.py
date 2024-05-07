# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

import numpy as np
import matplotlib.pyplot as plt

def plot_fit(time: np.array, dT: np.array, time_fit: np.array, dT_fit: np.array) -> None:
    plt.plot(time, dT, label = 'Simulation')
    plt.plot(time_fit, dT_fit, '--', c = 'r', label = 'Fit')
    plt.xlabel('Time[s]')
    plt.ylabel('$\Delta$T[K]')
    # plt.yscale('log')
    plt.show()

def plot_extracted(inverted_k: np.array, inverted_L: np.array, X_fit: np.array, y_fit: np.array, k_inf: float) -> None:
    plt.scatter(inverted_L, inverted_k, marker = '.')
    plt.scatter(0, 1 / k_inf, c = 'r', label = f'k_inf = {k_inf:.2f}')
    plt.plot(X_fit, y_fit, '--', c = 'r')
    plt.xlabel('1/L')
    plt.ylabel('1/k')
    plt.legend()
    plt.show()
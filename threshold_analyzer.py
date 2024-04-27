# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from analysis import extract_conductivity
import numpy as np
import matplotlib.pyplot as plt

# initialization
path = '../data/graphene/conductivity_shapes_final'
k_list = []
reduced_chi2_list = []
divs = np.linspace(0.25, 0.8, 48)     # 0.6 noted

# iterate
for div in divs:
    print(f'{div:.3f}')
    k, reduced_chi2 = extract_conductivity(path, div, [100, 1e-15])
    k_list.append(k)
    reduced_chi2_list.append(reduced_chi2)

# plot k trend
plt.plot(divs, k_list, marker = '.')
plt.ylabel('k')
plt.xlabel('Threshold')
plt.show()

# plot chi squared trend
plt.plot(divs, reduced_chi2_list, marker = '.')
plt.ylabel('$\chi^2$')
plt.xlabel('Threshold')
plt.show()
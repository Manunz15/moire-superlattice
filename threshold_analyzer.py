# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from analysis import extract_conductivity
import numpy as np
import matplotlib.pyplot as plt

# initialization
path = '../data/graphene/conductivity_angles/angle_1.50'
k_list = []
reduced_chi2_list = []
thresholds = np.linspace(0.25, 0.8, 12)     # 0.6 noted

# iterate
for threshold in thresholds:
    print(f'{threshold:.3f}')
    k, reduced_chi2 = extract_conductivity(path, threshold, [100, 1e-15])
    k_list.append(k)
    reduced_chi2_list.append(reduced_chi2)

# plot chi squared trend
plt.plot(thresholds, reduced_chi2_list, marker = '.')
plt.ylabel('$\chi^2$')
plt.xlabel('Threshold')
plt.show()

# plot k trend
plt.plot(thresholds, k_list, marker = '.')
plt.ylabel('k')
plt.xlabel('Threshold')
plt.show()
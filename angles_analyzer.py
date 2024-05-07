from analysis import extract_conductivity

import matplotlib.pyplot as plt
import os

# initialization
path = '../data/graphene/lv_conductivity/angles'
angle_list = []
k_list = []

# iterate
for dir in os.listdir(path):
    angle = float(dir.split('_')[-1])
    angle_list.append(angle)
    print(angle)

    k, chi2 = extract_conductivity(os.path.join(path, dir), 0.5, [100, 1e-12])
    k_list.append(k)

# plot k trend
plt.plot(angle_list, k_list, marker = 'o')
plt.ylabel('k')
plt.xlabel('Angle')
plt.yscale('log')
plt.show()
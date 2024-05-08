from analysis import ultimate_conductivity

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

    k, chi2 = ultimate_conductivity(os.path.join(path, dir), 0, [100, 1e-12], plot_final = True)
    k_list.append(k)

# plot k trend
plt.plot(angle_list, k_list, marker = 'o')
plt.ylabel('k')
plt.xlabel('Angle')
plt.show()
# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis import Lampin, ExtrConductivity, MoireConductivity

# lp = Lampin('../data/graphene/lv_conductivity/corrected_angles/angle_0.90/dim_6x1', 'graphene')
# print(lp)
# lp.plot_temp()
# lp.plot()

exco = ExtrConductivity('../data/graphene/lv_conductivity/corrected_angles/angle_1.00', 'graphene')
print(exco)

# for lp in exco.lampin_list:
#     lp.plot_temp()
#     lp.plot()
# moire = MoireConductivity('../data/graphene/lv_conductivity/corrected_angles', 'graphene')
# moire.plot()
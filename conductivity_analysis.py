# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis import Lampin, ExtrConductivity, MoireConductivity

# lp = Lampin('../data/graphene/lv_conductivity/corrected_angles/angle_1.10/dim_3x1', 'graphene')
# lp.plot_temp()
# lp.plot()

exco = ExtrConductivity('../data/graphene/lv_conductivity/corrected_angles/angle_1.10', 'graphene', plot = True)

# for lp in exco.lampin_list:
#     lp.plot_temp()
#     lp.plot()
# moire = MoireConductivity('../data/graphene/lv_conductivity/corrected_angles', 'graphene')
# moire.plot()
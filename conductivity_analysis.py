# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis import Lampin, ExtrConductivity, MoireConductivity

lp = Lampin('../data/graphene/lv_conductivity/corrected_angles/angle_0.90/dim_6x1', 'graphene')
lp.plot_temp()
lp.plot()
# moire = MoireConductivity('../data/graphene/lv_conductivity/corrected_angles', 'graphene')
# moire.plot()
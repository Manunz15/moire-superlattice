# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis import Lampin, ExtrConductivity, MoireConductivity

lp = Lampin('../data/graphene/lv_conductivity/monolayer/dim_100x60', 'graphene')
lp.plot()
lp.plot_temp()

# exco = ExtrConductivity('../data/graphene/lv_conductivity/monolayer', 'graphene')
# exco.plot()

# moire = MoireConductivity('../data/graphene/lv_conductivity/angles', 'graphene')
# moire.plot(err = True)
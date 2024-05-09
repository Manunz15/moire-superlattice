# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis import Lampin, ExtrConductivity, MoireConductivity

exco = ExtrConductivity('../data/graphene/lv_conductivity/onelayer', 'graphene', plot = True)
# exco.plot()
# moire = MoireConductivity('../data/graphene/lv_conductivity/angles', 'graphene')
# moire.plot()
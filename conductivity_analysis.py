# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis import Lampin, ExtrConductivity, MoireConductivity

exco = ExtrConductivity('../data/graphene/lv_conductivity/monolayer', 'graphene')
exco.plot()

moire = MoireConductivity('../data/graphene/lv_conductivity/corrected_angles', 'graphene')
moire.plot(err = True)
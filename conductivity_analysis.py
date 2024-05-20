# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis import Lampin, ExtrConductivity, MoireConductivity, Section

sec = Section('../data/graphene/lv_conductivity/test_section_1.50', 'graphene')
sec.plot()

exco = ExtrConductivity('../data/graphene/lv_conductivity/monolayer', 'graphene')
exco.plot()

moire = MoireConductivity('../data/graphene/lv_conductivity/angles', 'graphene')
moire.plot(err = True)
# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis import Lampin, ExtrConductivity, MoireConductivity, Section

sec = Section('../data/graphene/test_section_1.50', 'graphene')
sec.plot()

exco = ExtrConductivity('../data/graphene/monolayer', 'graphene')
exco.plot()

moire = MoireConductivity('../data/graphene/angles', 'graphene')
moire.plot(err = True)
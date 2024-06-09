# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis import Lampin, ExtrConductivity, MoireConductivity, Section

sec = Section('../data/graphene/almost_final/test_section_1.50', 'graphene')
sec.plot()

exco = ExtrConductivity('../data/graphene/almost_final/monolayer', 'graphene')
exco.plot()

moire = MoireConductivity('../data/graphene/almost_final/angles', 'graphene')
moire.plot(err = True)
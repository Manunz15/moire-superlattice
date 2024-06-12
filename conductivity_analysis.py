# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis import Lampin, ExtrConductivity, MoireConductivity, Section

lattice = 'graphene'

sec = Section(f'../data/{lattice}/test_section_1.50', 'graphene')
sec.plot()

# exco = ExtrConductivity(f'../data/{lattice}/monolayer', 'graphene')
# exco.plot()

# moire = MoireConductivity(f'../data/{lattice}/almost_final/angles', 'graphene')
# moire.plot(err = True)
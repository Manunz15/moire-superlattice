# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis import Lampin, ExtrConductivity, MoireConductivity, Section

lattice = 'LJ-graphene'

# sec = Section(f'../data/{lattice}/test_section_1.50', lattice)
# sec.plot()

# exco = ExtrConductivity(f'../data/{lattice}/monolayer', lattice)
# exco.plot()

# exco = ExtrConductivity(f'../data/{lattice}/angles/angle_0.00', lattice, 2)
# exco.plot()

moire = MoireConductivity(f'../data/{lattice}/angles', lattice)
moire.plot(err = True)
# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

from analysis import Lampin, ExtrConductivity, MoireConductivity, Section

lattice = 'h-BN'

# for n in [1, 2, 3, 4, 5, 10, 20, 50]:
    # lp = Lampin(f'../data/{lattice}/AA stack/dim_40x120', lattice, num_exp = n) # save_path = '../latex/graphs/data/temp-LJ-bilayer')
# lp.save('../latex/graphs/data/k-t/bilayer_LJ_40x120')
# lp.plot_temp()

# lp = Lampin(f'../data/{lattice}/monolayer/dim_40x120', lattice, 1)
# print(f'L = {lp.L / 10:.1f}, d = {lp.S / 33.5:.1f}, S = {lp.S / 100:.1f}')
# lp.plot()

# sec = Section(f'../data/{lattice}/test_section_1.50', lattice, num_layers = 1)
# sec.save('../latex/graphs/data/sec/monolayer')
# sec.plot()

# exco = ExtrConductivity(f'../data/{lattice}/AA stack', lattice, 2)
# exco.save('../latex/graphs/data/k-inf/LJ-0.00')
# exco.plot()
# exco.plot_lasso()

# exco = ExtrConductivity(f'../data/{lattice}/monolayer', lattice, num_layers = 1)
# exco.save('../latex/graphs/data/moire/uncoupled monolayer', True)

# exco = ExtrConductivity(f'../data/{lattice}/AA stack', lattice)
# exco.save('../latex/graphs/data/moire/uncoupled AA stack', True)

# exco = ExtrConductivity(f'../data/{lattice}/AB stack', lattice)
# exco.save('../latex/graphs/data/moire/uncoupled AB stack', True)

moire = MoireConductivity(f'../data/{lattice}/angles', lattice, num_layers = 2)
moire.save('../latex/graphs/data/moire/hbn moire')
moire.plot(err = True)
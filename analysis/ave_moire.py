from analysis.moire import MoireConductivity
import matplotlib.pyplot as plt

class AverageMoire:
    def __init__(self, paths: list[str], lattice: str, num_layers: int = 2) -> None:
        self.paths: list[str] = paths
        self.lattice: str = lattice
        self.num_layers: int = num_layers

        self.moires: list[MoireConductivity] = []
        self.dict: dict[float, dict[str, list[float]]] = {}

        self.angle_list: list[float] = []
        self.k_list: list[float] = []
        self.err_list: list[float] = []

        self.calc_moire()
        self.average_moire()

    def calc_moire(self):
        for path in self.paths:
            self.moires.append(MoireConductivity(path, self.lattice, self.num_layers))

        for moire in self.moires:
            for angle, k, err in zip(moire.angle_list, moire.k_list, moire.err_list):
                # save k
                if angle in self.dict.keys():
                    self.dict[angle]['k'].append(k)
                    self.dict[angle]['err'].append(err)
                else:
                    self.dict[angle] = {'k': [k], 'err': [err]}

    def average_moire(self):
        for angle, k_dict in self.dict.items():
            self.angle_list.append(angle)
            self.k_list.append(sum(k_dict['k']) / len(k_dict['k']))
            self.err_list.append(k_dict['err'][0] if len(k_dict['err']) == 1 else (max(k_dict['k']) - min(k_dict['k']))/2)

    def plot(self, err = True, small = True):
        if small:
            for moire in self.moires:
                moire.plot(err = err, hold = True)

        if err:
            plt.errorbar(self.angle_list, self.k_list, yerr = self.err_list, marker = 'o', zorder = len(self.moires))
        else:
            plt.plot(self.angle_list, self.k_list, marker = 'o', zorder = len(self.moires))

        plt.xlabel(r'$\theta$°')
        plt.ylabel(r'k[W/K$\cdot$m]')
        plt.show()
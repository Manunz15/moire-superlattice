# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from lattice.atomsplot import AtomsPlot
from lattice.transform import Transform
from lattice.presets import lattices
from utils.setting import K_B, uma
from utils.today import today

class Lattice:
    def __init__(self, lattice: str, name: str = None, atoms: pd.DataFrame = None, filename: str = None) -> None:
        # initialization
        self.lattice = lattice
        self.name = name if name else lattice
        self.box = [(0, 0)] * 3

        # properties
        if lattice in lattices:
            self.potential = lattices[lattice]['potential']
            self.step: float = lattices[lattice]['step']
            self.z_step: float = lattices[lattice]['z_step']
            self.atom_types: dict[str, dict] = lattices[lattice]['atom_types']
            self.to_interchange: bool = lattices[lattice]['to_interchange']
            self.box_pad = [self.step, self.step * np.sin(np.pi / 3), 1e4]
        else:
            raise NameError(f"'{lattice}' is not a defined lattice, please change lattice or add data for '{lattice}' in <presets.py>.")

        # read filename
        if filename:
            self.read(filename)
        else:
            self.add(atoms)
            self.create_box()

    def __str__(self) -> str:
        try:
            incipit = f'{self.name}: {len(self.atoms)} atoms'
        except:
            incipit = self.name

        return f'{incipit}\nbox: {self.box}'
    
    def rename(self, name: str):
        self.name = name

    def add(self, atoms: pd.DataFrame) -> None:
        self.atoms = atoms

    def center(self) -> list:
        self.translate([- self.atoms[xi].mean() for xi in ['x', 'y', 'z']])

    def create_box(self, pad: list[float] = None) -> None:
        """
        CREATE BOX
        -------------------------------------------------------------------------
        This function is used to create boxes for LAMMPS simulations.

        The box is created such that:
        1. It contains all the atoms contained in the 'DF' pandas dataframe;
        2. Its edges are parallel to the x,y,z axes;
        3. Its volume is minimized with the above two points satisfied.

        Its faces can be expanded thanks to a 'delta' list (default = [0, 0, 0]).
        Where the first element 'delta[0]' adds 'delta[0] / 2' units on the left 
        and 'delta[0] / 2' units on the right of the x-dimension of the box. The 
        same is true between the second (third) element and the y(z)-dimension.

        For example if the box initially spans from 0 to 5 in the x-axis and delta[0] 
        is 10,then the new box x-dimension will span from -5 to 10.
        """
        
        # define pad
        if not pad:
            pad = self.box_pad
        else:
            self.box_pad = pad

        # create box
        try:
            xlo, xhi = self.atoms['x'].min() - pad[0] / 2, self.atoms['x'].max() + pad[0] / 2
            ylo, yhi = self.atoms['y'].min() - pad[1] / 2, self.atoms['y'].max() + pad[1] / 2
            zlo, zhi = self.atoms['z'].min() - pad[2] / 2, self.atoms['z'].max() + pad[2] / 2

            self.box = [(xlo, xhi), (ylo, yhi), (zlo, zhi)]
        except:
            pass

    def velocity(self, T: float = 300) -> None:
        # create velocity columns
        for vi in ['vx', 'vy', 'vz']:
            if vi not in self.atoms.columns:
                self.atoms.insert(len(self.atoms.columns), vi, np.zeros(len(self.atoms)), True)

        if T == 0:
            return 0            

        for atom_properties in self.atom_types.values():    
            # initialization        
            m = atom_properties['mass'] * uma
            len_v = int(1e4)
            len_random = int(len(self.atoms[self.atoms['type'] == atom_properties['id']]))

            # velocity distribution
            v = np.linspace(0, 15000, len_v)
            dv = np.full(len_v, fill_value = v[1] - v[0])
            fv = 4 * np.pi * (v ** 2) * (m / (2 * np.pi * K_B * T)) ** 1.5 * np.exp(- m * (v ** 2) / (2 * K_B * T)) 

            # inverse trasform sampling
            integral = np.zeros(len(fv))
            for index in range(len(fv)):
                integral[index] = np.dot(fv[:index], dv[:index])

            # generate velocities
            random_num = np.random.random(len_random)
            random_v = np.zeros(len_random)
            for index, num in enumerate(random_num):
                random_v[index] = v[np.argmin(abs(integral - num))]

            # convert in argstrom / picoseconds
            random_v /= 100

            # random angles
            random_angles = 2 * np.pi * np.random.random(len_random)
            random_cos = np.cos(random_angles)
            random_sin = np.sin(random_angles)
            random_vx = random_v * random_cos
            random_vy = random_v * random_sin

            # save velocities
            self.atoms.loc[self.atoms['type'] == atom_properties['id'], 'vx'] = random_vx
            self.atoms.loc[self.atoms['type'] == atom_properties['id'], 'vy'] = random_vy

    def plot(self, projection: str = '2d') -> None:
        AtomsPlot(atoms = self.atoms, name = self.name, projection = projection)
    
    def plot_velocity(self) -> None:
        vx = self.atoms['vx'].to_numpy()
        vy = self.atoms['vy'].to_numpy()
        vz = self.atoms['vz'].to_numpy()

        v = np.sqrt(vx**2 + vy**2 + vz**2)
        plt.hist(v, bins = 50, rwidth = 0.8)
        plt.xlabel('v[Å/ps]')
        plt.ylabel('Number of atoms')
        plt.show()

    def translate(self, trasl: list) -> None:
        Transform().translate(self.atoms, trasl = trasl)

    def rotate(self, angle: float, center: bool = True) -> None:
        Transform().rotate(self.atoms, angle = angle, center = center)

    def interchange(self) -> None:
        Transform().permutate(self.atoms, perm = {1:2})

    def drop(self, cut_box: list[tuple]) -> None:
        min_point = cut_box[0]
        max_point = cut_box[1]
        
        for pos, coord in zip(min_point, ['x', 'y', 'z']):
            self.atoms = self.atoms[self.atoms[coord] > pos]

        for pos, coord in zip(max_point, ['x', 'y', 'z']):
            self.atoms = self.atoms[self.atoms[coord] < pos]

    def read(self, filename: str) -> None:
        # initialization
        read: bool = False
        read_box: int = 0

        # read file
        with open(filename, 'r') as f:
            for line in f:
                # box line
                if 'ITEM: BOX' in line:
                    read_box = 3

                # read box
                elif read_box:
                    self.box[3 - read_box] = tuple(map(float, line.split()))
                    read_box -= 1

                # columns line
                elif 'ITEM: ATOMS' in line:
                    read: bool = True
                    DATA: list[float] = []
                    COLUMNS: list[float] = line.split()[2:]
                    
                # read data
                elif read:
                    DATA.append(list(map(float, line.split()))) 

        self.add(pd.DataFrame(DATA, columns = COLUMNS))

    def write(self, filename: str) -> None:
        f = open(filename, 'w')

        # initial comment
        f.write(f'# Lorenzo Manunza {today()}\n\n')

        # number of atoms
        self.atoms
        f.write(f'{len(self.atoms)} atoms\n{len(self.atom_types)} atom types\n\n')

        # box dimensions
        x, y, z = self.box
        f.write(f'{x[0]:.2f} {x[1]:.2f} xlo xhi\n')
        f.write(f'{y[0]:.2f} {y[1]:.2f} ylo yhi\n')
        f.write(f'{z[0]:.2f} {z[1]:.2f} zlo zhi\n')

        # masses
        f.write('\nMasses\n\n')

        for atom_type in self.atom_types:
            f.write(f'{self.atom_types[atom_type]["id"]} {self.atom_types[atom_type]["mass"]} # {atom_type}\n')

        # atoms
        f.write('\nAtoms\n\n')
        f.write(f'{self.atoms[["id", "type", "x", "y", "z"]].to_string(header = False, index = False, index_names = False)}')

        # velocities
        if 'vx' in self.atoms.keys():
                f.write('\n\nVelocities\n\n')
                f.write(f'{self.atoms[["id", "vx", "vy", "vz"]].to_string(header = False, index = False, index_names = False)}')

        f.close()
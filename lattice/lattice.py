# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from lattice.atomsplot import AtomsPlot
from lattice.transform import Transform as tr
from lattice.presets import lattices
from utils.settings import K_B, ang2bohr
from utils.time import today
from utils.execute import execute

class Lattice:
    def __init__(self, lattice: str, name: str = None, atoms: pd.DataFrame = None, filename: str = None) -> None:
        # initialization
        self.lattice = lattice
        self.name = name if name else lattice
        self.box = [(0, 0)] * 3
        self.units = 'angstrom'

        # properties
        if lattice in lattices:
            self.potential = lattices[lattice]['potential']
            self.step: float = lattices[lattice]['step']
            self.z_step: float = lattices[lattice]['z_step']
            self.atom_types: dict[str, dict] = lattices[lattice]['atom_types']
            self.num_types: int = len(self.atom_types)
            self.to_interchange: bool = lattices[lattice]['to_interchange']
            self.full: bool = lattices[lattice]['full']
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

        # create box if it doesn't exist
        if self.box == [(0, 0)] * 3:
            self.create_box()

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

    def calculate_gr(self) -> None:
        pass

    def centering(self) -> None:
        self.translate([- self.atoms['x'].mean(), - self.atoms['y'].mean(), - self.atoms['z'].mean()])

    def align_to_bl(self) -> None:
        self.translate([- self.atoms['x'].min(), - self.atoms['y'].min(), - self.atoms['z'].min()])

    def scale(self, factor: float) -> None:
        tr.scale(self.atoms, factor = factor)
        self.box = [(self.box[0][0] * factor, self.box[0][1] * factor),
                    (self.box[1][0] * factor, self.box[1][1] * factor),
                    (self.box[2][0] * factor, self.box[2][1] * factor),]
        
    def translate(self, trasl: list[float]) -> None:
        tr.translate(self.atoms, trasl = trasl)
        self.box = [(self.box[0][0] + trasl[0], self.box[0][1] + trasl[0]),
                    (self.box[1][0] + trasl[1], self.box[1][1] + trasl[1]),
                    (self.box[2][0] + trasl[2], self.box[2][1] + trasl[2]),]

    def rotate(self, angle: float) -> None:
        tr.rotate(self.atoms, angle = angle)

    def interchange(self) -> None:
        tr.permutate(self.atoms, perm = {1:2})

    def angstrom_to_bohr(self) -> None:
        if self.units == 'angstrom':
            self.scale(ang2bohr)
            self.units = 'bohr'

    def bohr_to_angstrom(self) -> None:
        if self.units == 'bohr':
            self.scale(1 / ang2bohr)
            self.units = 'angstrom'

    def cut(self, cut_box: list[tuple]) -> None:
        min_point = cut_box[0]
        max_point = cut_box[1]
        
        for pos, coord in zip(min_point, ['x', 'y', 'z']):
            self.atoms = self.atoms[self.atoms[coord] >= pos]

        for pos, coord in zip(max_point, ['x', 'y', 'z']):
            self.atoms = self.atoms[self.atoms[coord] < pos]

        self.atoms['id'] = np.arange(1, len(self.atoms) + 1)
        self.atoms.reset_index(drop=True, inplace=True)

    def remove_overlapping_atoms(self) -> None:
        self.write_lammps('lattice/remove_overlapping/atoms.dat')

        # remove overlapping atoms
        execute(Windows = 'cd lattice/remove_overlapping && lmp -in in.REMOVE',
                Linux = 'cd lattice/remove_overlapping && bash remove.sh')
        self.read('lattice/remove_overlapping/new.atoms')

        # remove files
        execute(Windows = r'del .\lattice\remove_overlapping\atoms.dat',
                Linux = 'rm lattice/remove_overlapping/atoms.dat')
        execute(Windows = r'del .\lattice\remove_overlapping\log.lammps',
                Linux = 'rm lattice/remove_overlapping/log.lammps')
        execute(Windows = r'del .\lattice\remove_overlapping\new.atoms',
                Linux = 'rm lattice/remove_overlapping/new.atoms')

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

    def write_lammps(self, filename: str) -> None:
        # centering 
        self.centering()
        
        f = open(filename, 'w')

        # initial comment
        f.write(f'# Lorenzo Manunza {today()}\n\n')

        # number of atoms
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
        cols = ['id', 'type', 'x', 'y', 'z']
        if self.full:
            self.atoms.insert(1, 'molecule', np.zeros(len(self.atoms)).astype(int), True)
            self.atoms.insert(3, 'q', np.zeros(len(self.atoms)).astype(int), True)
            cols = ['id', 'molecule', 'type', 'q', 'x', 'y', 'z']
        f.write('\nAtoms\n\n')
        f.write(f'{self.atoms[cols].to_string(header = False, index = False, index_names = False)}')

        # velocities
        if 'vx' in self.atoms.keys():
            f.write('\n\nVelocities\n\n')
            f.write(f'{self.atoms[["id", "vx", "vy", "vz"]].to_string(header = False, index = False, index_names = False)}')

        f.close()

    def write_alm(self, filename: str) -> None:
        # remove overlapping atoms
        self.remove_overlapping_atoms()

        f = open(filename, 'w')

        # initial comment
        f.write(f'# Lorenzo Manunza {today()}\n\n')

        # general
        f.write(f'&general\n\tPREFIX = {self.lattice}\n\tMODE = suggest\n\tNAT = {len(self.atoms)}; NKD = {len(self.atom_types)}\n\tKD = C\n/\n\n')

        # interaction
        f.write(f'&interaction\n\tNORDER = 1  # 1: harmonic, 2: cubic, ..\n/\n\n')

        # cell
        self.align_to_bl()
        self.angstrom_to_bohr()
        a1 = self.box[0][1] - self.box[0][0]
        a2 = self.box[1][1] - self.box[1][0]
        a3 = self.box[2][1] - self.box[2][0]

        self.atoms['type'] = self.atoms['type'].astype(int)
        f.write(f'&cell\n\t{a1} # factor in Bohr\n\t1.0 0.0 0.0 # a1\n\t0.0 {a2 / a1} 0.0 # a2\n\t0.0 0.0 {a3 / a1} # a3\n/\n\n')

        # cutoff
        f.write(f'&cutoff\n\t*-* {5.0 * ang2bohr}\n/\n\n')

        # position
        for xi, ai in zip(['x', 'y', 'z'], [a1, a2, a3]):
            self.atoms[xi] = self.atoms[xi] / ai
        f.write(f'&position\n{self.atoms[["type", "x", "y", "z"]].to_string(header = False, index = False, index_names = False)}')

        # close
        f.close()
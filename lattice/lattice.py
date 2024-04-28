# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

import numpy as np
import pandas as pd

from lattice.atomsplot import AtomsPlot
from lattice.transform import Transform
from lattice.presets import lattices
from utils.today import today

class Lattice:
    def __init__(self, lattice: str, name: str = None, atoms: pd.DataFrame = None) -> None:
        # initialization
        self.lattice = lattice
        self.name = name if name else lattice

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
        
        # atoms
        self.add(atoms = atoms)

    def __str__(self) -> str:
        return self.name
    
    def rename(self, name: str):
        self.name = name

    def add(self, atoms: pd.DataFrame) -> None:
        self.atoms = atoms
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
    
    def translate(self, trasl: list) -> None:
        Transform().translate(self.atoms, trasl = trasl)

    def rotate(self, angle: float) -> None:
        Transform().rotate(self.atoms, angle = angle)

    def interchange(self) -> None:
        Transform().permutate(self.atoms, perm = {1:2})

    def write(self, filename: str) -> None:
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
        f.write('\nAtoms\n\n')
        f.write(f'{self.atoms[["id", "type", "x", "y", "z"]].to_string(header = False, index = False, index_names = False)}')

        # velocities
        if 'vx' in self.atoms.keys():
                f.write('\n\nVelocities\n\n')
                f.write(f'{self.atoms[["id", "vx", "vy", "vz"]].to_string(header = False, index = False, index_names = False)}')

        f.close()
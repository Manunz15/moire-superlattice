# Lorenzo Manunza, Università degli Studi di Cagliari, March 2024

import pandas as pd

class WriteAtoms:
    def __init__(self):
        pass

    def write(self, DF: pd.DataFrame, elements: dict, filename: str, box: list[tuple[float]], title: str = 'a comment'):
        f = open(filename, 'w')

        # initial comment
        f.write(f'# {title}\n\n')

        # number of atoms
        f.write(f'{len(DF)} atoms\n{len(elements)} atom types\n\n')

        # box dimensions
        x, y, z = box
        f.write(f'{x[0]:.2f} {x[1]:.2f} xlo xhi\n')
        f.write(f'{y[0]:.2f} {y[1]:.2f} ylo yhi\n')
        f.write(f'{z[0]:.2f} {z[1]:.2f} zlo zhi\n')

        # masses
        f.write('\nMasses\n\n')

        for element in elements:
            f.write(f'{elements[element]["id"]} {elements[element]["mass"]} # {element}\n')

        # atoms
        f.write('\nAtoms\n\n')
        f.write(f'{DF[["id", "type", "x", "y", "z"]].to_string(header = False, index = False, index_names = False)}')

        # velocities
        if 'vx' in DF.keys():
                f.write('\n\nVelocities\n\n')
                f.write(f'{DF[["id", "vx", "vy", "vz"]].to_string(header = False, index = False, index_names = False)}')

        f.close()
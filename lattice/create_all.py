# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from copy import copy
import os

from lattice.hex import HexLattice
from lattice.lattice import Lattice 
from lattice.presets import lattices
from lattice.add_layers import add_layers
from utils.file import replace
from utils.path import Path

def create_all(lattice: str, lammps: str, dir_name: str, DIMS: list[tuple], ANGLES: list[float] = None, 
               double: bool = False, plot: str = None) -> None:
    
    # files to copy
    files: list = copy(lattices[lattice]['potential'])
    files = files if type(files) == list else [files]
    files.append(lammps)
    filenames = [os.path.join('lammps', lattice, file) for file in files]

    DIMS = DIMS if type(DIMS) == list else [DIMS]

    # iterate for shape
    for dim in DIMS:        
        if len(DIMS) == 1:
            dim_dir = ''
            dir_name = f'{dir_name}_{dim[0]}x{dim[1]}'
        else:
            dim_dir = f'dim_{dim[0]}x{dim[1]}'
        
        # if angles are specified
        if ANGLES:
            for angle in ANGLES:
                lt = HexLattice(lattice = lattice, dim = dim, angle = angle)
                
                angle_dir = '' if len(ANGLES) == 1 else f'angle_{angle:.2f}'
                path = Path(path = [lt.lattice, dir_name, angle_dir, dim_dir])
                save(lt, filenames, path, plot)
                
        # if angles are NOT specified
        else:
            lt = HexLattice(lattice = lattice, dim = dim)

            box_pad = lt.box_pad
            lt.rotate(90)
            lt.centering()
            if double:
                lt = add_layers(lt, angle = 0)
                
            lt.create_box([box_pad[1], box_pad[0], box_pad[2]])
            
            path = Path(path = [lt.lattice, dir_name, dim_dir])
            save(lt, filenames, path, plot)

def save(lattice: Lattice, filenames: list[str], path: Path, plot: str) -> None:
    # save
    print(path)
    path.copy(filenames = filenames)
    
    if abs(lattice.box[0][1] + lattice.box[0][0]) > 0.01:
        raise Warning('The box is not perfectly symmetrical')
    
    lattice.write_lammps(filename = os.path.join(path.path, 'atoms.dat'))

    # plot
    if plot:
        lattice.plot(projection = plot)
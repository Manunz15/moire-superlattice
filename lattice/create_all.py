# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

from lattice.hex import HexLattice
from lattice.lattice import Lattice 
from lattice.presets import lattices
from lattice.add_layers import add_layers
from utils.file import replace
from utils.path import Path

def save(lattice: Lattice, filenames: list[str], path: Path, lammps: str, plot: bool) -> None:
    # box
    replacements = {'x_1i': round(lattice.box[0][0], 3),
            'x_1f': round((lattice.box[0][1] - lattice.box[0][0]) / 2, 3),
            'x_2i': round((lattice.box[0][1] - lattice.box[0][0]) / 2 + 0.1, 3),
            'x_2f': round(lattice.box[0][1], 3)}

    # save
    print(path)
    path.copy(filenames = filenames)
    replace(filename = '/'.join([path.path, lammps]), replacements = replacements)
    lattice.write(filename = f'{path.path}/atoms.dat')
    
    # plot
    if plot:
        lattice.plot()

def create_all(lattice: str, DIMS: list[tuple], ANGLES: list[float] = None, dir_name: str = '', lammps: str = 'in.CONDUCTIVITY', plot: bool = False) -> None:
    # files to copy
    filenames = ['/'.join(['lammps', lattice, lattices[lattice]['potential']]),
         '/'.join(['lammps', lattice, lammps])]
    
    if type(DIMS) != list:
        DIMS = [DIMS]

    # iterate for shape
    for dim in DIMS:
        lt = HexLattice(lattice = lattice, dim = dim)
        
        if len(DIMS) == 1:
            dim_dir = ''
            dir_name = f'{dir_name}_{dim[0]}x{dim[1]}'
        else:
            dim_dir = f'dim_{dim[0]}x{dim[1]}'
        
        # if angles are specified
        if ANGLES:
            for angle in ANGLES:
                new_lt = add_layers(lattice = lt, angle = angle)
                angle_dir = '' if len(ANGLES) == 1 else f'angle_{angle:.2f}'
                path = Path(path = [new_lt.lattice, dir_name, angle_dir, dim_dir])
                save(new_lt, filenames, path, lammps, plot)
        
        # if angles are NOT specified
        else:
            path = Path(path = [lt.lattice, dir_name, dim_dir])
            save(lt, filenames, path, lammps, plot)
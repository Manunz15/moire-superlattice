from lattice import HexLattice, create_all, Lattice

# twisted double layer
DIMS = [(width, 1) for width in range(1, 5)]
ANGLES = [0.9, 1.0, 1.1, 1.2, 1.3, 1.5]
# create_all(lattice = 'graphene', DIMS = DIMS, ANGLES = ANGLES, dir_name = 'lv_conductivity/angles', lammps = 'in.LV_CONDUCTIVITY')

# onelayer and bilayer
width = 60
DIMS = [(width, height) for height in range(100, 180 + 1, 20)]
# create_all(lattice = 'graphene', DIMS = DIMS, dir_name = 'lv_conductivity/onelayer', lammps = 'in.LV_CONDUCTIVITY')
create_all(lattice = 'graphene', DIMS = DIMS, double = True, dir_name = 'lv_conductivity/rot_bilayer', lammps = 'in.LV_CONDUCTIVITY', plot = '2d')
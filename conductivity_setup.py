from lattice import HexLattice, create_all, Lattice

# twisted double layer
# DIMS = [(width, 1) for width in range(1, 7)]
# ANGLES = [0.6, 0.8]
# create_all(lattice = 'graphene', DIMS = DIMS, ANGLES = ANGLES, dir_name = 'lv_conductivity/more_angles', lammps = 'in.LV_CONDUCTIVITY')

# onelayer and bilayer
height = 100
DIMS = [(width, height) for width in range(70, 130 + 1, 20)]
# create_all(lattice = 'graphene', DIMS = DIMS, dir_name = 'lv_conductivity/onelayer', lammps = 'in.LV_CONDUCTIVITY')
create_all(lattice = 'graphene', DIMS = DIMS, double = True, dir_name = 'lv_conductivity/more_bilayer', lammps = 'in.LV_CONDUCTIVITY')
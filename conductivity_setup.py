from lattice import HexLattice, create_all, Lattice

lattice = 'graphene'

# twisted double layer
DIMS = [(width, 1) for width in range(1, 7 + 1)]
ANGLES = [0.6, 0.8]
create_all(lattice = lattice, DIMS = DIMS, ANGLES = ANGLES, dir_name = 'lv_conductivity/small_angles', lammps = 'in.LONG_LV_CONDUCTIVITY')

ANGLES = [0.9, 1.0, 1.05, 1.08, 1.1, 1.2, 1.3, 1.5]
create_all(lattice = lattice, DIMS = DIMS, ANGLES = ANGLES, dir_name = 'lv_conductivity/big_angles', lammps = 'in.LV_CONDUCTIVITY')

# test section
DIMS = [(1, height) for height in range(1, 7 + 1)]
ANGLES = [1.5]
create_all(lattice = lattice, DIMS = DIMS, ANGLES = ANGLES, dir_name = 'lv_conductivity/test_section', lammps = 'in.LV_CONDUCTIVITY')

# monolayer and bilayer
# width, height = 100, 60
# DIMS = [(width * n, height) for n in range(1, 7 + 1)]
# create_all(lattice = lattice, DIMS = DIMS, dir_name = 'lv_conductivity/monolayer', lammps = 'in.LV_CONDUCTIVITY')

# width, height = 40, 120
# DIMS = [(width, height * n) for n in range(1, 7 + 1)]
# create_all(lattice = lattice, DIMS = DIMS, double = True, dir_name = 'lv_conductivity/bilayer', 
#            lammps = 'in.LV_CONDUCTIVITY', rot = True)
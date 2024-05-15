from lattice import HexLattice, create_all, Lattice

# twisted double layer
# DIMS = [(width, 1) for width in range(1, 7)]
# ANGLES = [0.6, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5]
# create_all(lattice = 'graphene', DIMS = DIMS, ANGLES = ANGLES, dir_name = 'lv_conductivity/angles', lammps = 'in.LV_CONDUCTIVITY')

# monolayer and bilayer
width = 100
height = 60
DIMS = [(width * n, height) for n in range(1, 6+ 1)]
create_all(lattice = 'graphene', DIMS = DIMS, dir_name = 'lv_conductivity/corrected_monolayer', lammps = 'in.LV_CONDUCTIVITY')

width = 40
height = 120
DIMS = [(width, height * n) for n in range(1, 6 + 1)]
create_all(lattice = 'graphene', DIMS = DIMS, double = True, dir_name = 'lv_conductivity/corrected_bilayer', 
           lammps = 'in.LV_CONDUCTIVITY', rot = True)
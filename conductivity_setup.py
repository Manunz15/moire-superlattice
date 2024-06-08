from lattice import HexLattice, create_all, Lattice

lattice = 'graphene'
lammps = 'in.LV_CONDUCTIVITY'
long_lammps = 'in.LONG_LV_CONDUCTIVITY'

# twisted double layer
DIMS = [(width, 1) for width in range(1, 7 + 1)]
ANGLES = [0.6, 0.8]
create_all(lattice = lattice, DIMS = DIMS, ANGLES = ANGLES, dir_name = 'small_angles', lammps = long_lammps)

ANGLES = [0.9, 1.0, 1.05, 1.08, 1.1, 1.2, 1.3, 1.5]
create_all(lattice = lattice, DIMS = DIMS, ANGLES = ANGLES, dir_name = 'big_angles', lammps = lammps)

# test section
DIMS = [(1, height) for height in range(1, 7 + 1)]
ANGLES = [1.5]
create_all(lattice = lattice, DIMS = DIMS, ANGLES = ANGLES, dir_name = 'test_section_1.50', lammps = lammps)

# monolayer and bilayer
width, height = 100, 60
DIMS = [(width * n, height) for n in range(1, 7 + 1)]
create_all(lattice = lattice, DIMS = DIMS, dir_name = 'monolayer', lammps = lammps)

width, height = 40, 120
DIMS = [(width, height * n) for n in range(1, 7 + 1)]
create_all(lattice = lattice, DIMS = DIMS, double = True, dir_name = 'bilayer', 
           lammps = lammps, rot = True)
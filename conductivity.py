from lattice import HexLattice, create_all, Lattice

# twisted double layer
DIMS = [(width, 1) for width in range(1, 5)]
ANGLES = [0.9, 1.0, 1.1, 1.2, 1.3, 1.5]
create_all(lattice = 'graphene', DIMS = DIMS, ANGLES = ANGLES, dir_name = 'conductivity_angles', lammps = 'in.CONDUCTIVITY')

# onelayer and bilayer
height = 100
DIMS = [(width, height) for width in range(60, 140 + 1, 20)]
create_all(lattice = 'graphene', DIMS = DIMS, dir_name = 'conductivity_onelayer', lammps = 'in.CONDUCTIVITY')
create_all(lattice = 'graphene', DIMS = DIMS, double = True, dir_name = 'conductivity_bilayer', lammps = 'in.CONDUCTIVITY')
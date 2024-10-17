from lattice import HexLattice, create_all, Lattice

lattice = 'LJ-graphene'
lammps = 'in.LV_CONDUCTIVITY_II'

# twisted double layer
DIMS = [(width, 1) for width in range(1, 7 + 1)]
ANGLES = [1.08, 1.12, 1.2, 1.3, 1.5]
create_all(lattice = lattice, DIMS = DIMS, ANGLES = ANGLES, dir_name = 'even_more_data', lammps = lammps)
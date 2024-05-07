#!/bin/bash/

# Lorenzo Manunza, Università degli Studi di Cagliari, May 2024

# run in.REMOVE
eval "$(conda shell.bash hook)"
conda activate my-lammps
export OMP_NUM_THREADS=1
mpirun -np 56 lmp -in in.REMOVE
conda deactivate	
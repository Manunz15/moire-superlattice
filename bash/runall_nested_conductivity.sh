#!/bin/bash/

# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

# paths
lattice="graphene"
dir_name="dir_name"
path="../../simulations/$lattice/$dir_name/*/"
base=$(pwd)

# iterating in folders
for dir in $path
do  
    # iterating in sub-folders 
    for sub_dir in "${dir}"*
    do
        # running
        cd $sub_dir
        echo $sub_dir
        eval "$(conda shell.bash hook)"
        conda activate my-lammps
        export OMP_NUM_THREADS=1
        mpirun -np 56 lmp -in in.LV_CONDUCTIVITY
        conda deactivate	
        cd $base
    done
done

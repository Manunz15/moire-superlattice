#!/bin/bash/

# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

# paths
path="../../simulations/graphene/best_method/*/"
base=$(pwd)

# iterating in folders
for dir in $path
do
	dir="${dir}*/"
	for sub_dir in $dir
	do
		# running
		cd $sub_dir
		echo $sub_dir
		eval "$(conda shell.bash hook)"
		conda activate my-lammps
		export OMP_NUM_THREADS=1
		mpirun -np 56 lmp -in in.TO_300K
		conda deactivate	
		cd $base
	done
done

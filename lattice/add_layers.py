# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

import pandas as pd
from copy import deepcopy

from lattice.lattice import Lattice

def merge(first_lattice: Lattice, second_lattice: Lattice, name: str = None) -> Lattice:
    # copy 
    first_lattice = deepcopy(first_lattice)
    second_lattice = deepcopy(second_lattice)

    # lattices must be of the same type
    lattice = first_lattice.lattice
    if first_lattice.lattice != second_lattice.lattice:
        raise TypeError('Lattices must be of the same type.')
    
    # concatenate atoms
    second_lattice.atoms['id'] += len(first_lattice.atoms)
    final_atoms = pd.concat([first_lattice.atoms, second_lattice.atoms], ignore_index = True)

    return Lattice(lattice = lattice, name = name, atoms = final_atoms)

def add_layers(lattice: Lattice, angle: float = 0, num_layers: int = 2) -> Lattice:
    # copy lattice
    new_lattice = deepcopy(lattice)
    new_lattice.rotate(angle = (1 - num_layers) * angle / 2)

    # new layer
    new_layer = deepcopy(new_lattice)

    # add new layers
    for _ in range(1, num_layers):
        if new_layer.to_interchange:
            new_layer.interchange()
            
        new_layer.rotate(angle = angle)
        new_layer.translate(trasl = [0, 0, lattice.z_step])
        new_lattice = merge(first_lattice = new_lattice, second_lattice = new_layer)

    return new_lattice
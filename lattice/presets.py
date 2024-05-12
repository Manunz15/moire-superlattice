# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

lattices = {
    # source: https://en.wikipedia.org/wiki/Graphite#Structure 22/04/2024
    'graphene': {
        'potential': 'CH.airebo',
        'step': 1.42,
        'z_step': 3.35,
        'T_debye': 1813,
        'atom_types': {'C': {'id': 1, 'mass': 12.011}},
        'to_interchange': False
    },
    # source: place holder
    'h-BN': {
        'potential': 'BNC.tersoff',
        'step': 1.446,
        'z_step': 3.335,
        'atom_types': {'B': {'id': 1, 'mass': 10.811},
                       'N': {'id': 2, 'mass': 14.0067}},
        'to_interchange': True
    },}
# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

lattices = {
    # source: https://en.wikipedia.org/wiki/Graphite#Structure 22/04/2024
    'graphene': {
        'potential': 'CH.airebo',
        'step': 1.42,
        'z_step': 3.35,
        'atom_types': {'C': {'id': 1, 'mass': 12.011}},
        'to_interchange': False,
        'full': False
    },
    # step source: place holder
    # z step source: https://link.springer.com/article/10.1007/s11249-018-1078-y
    'h-BN': {
        'potential': ['ffield.reax.AB', 'lmp_control', 'param.qeq'],
        'step': 1.45,
        'z_step': 3.35,
        'atom_types': {'B': {'id': 1, 'mass': 10.811},
                       'N': {'id': 2, 'mass': 14.0067}},
        'to_interchange': True,
        'full': True
    },}
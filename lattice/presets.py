# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

lattices = {
    # source: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6116708/ and https://en.wikipedia.org/wiki/Graphite#Structure
    'graphene': {
        'potential': 'CH.airebo',
        'step': 1.42,
        'z_step': 3.35,
        'err': 0.08,
        'z_step_after': 3.29,
        'atom_types': {'C': {'id': 1, 'mass': 12.011}},
        'to_interchange': False,
        'full': False
    },
    # step source: https://www.nature.com/articles/s41467-021-26072-7
    # z step source: https://www.sciencedirect.com/science/article/abs/pii/S0025540815300088
    'h-BN': {
        'potential': ['BNC.tersoff', 'BNCH.ILP'],
        'step': 1.45,
        'z_step': 3.33,
        'err': 0.07,
        'z_step_after': 3.32,
        'atom_types': {'B': {'id': 1, 'mass': 10.811},
                       'N': {'id': 2, 'mass': 14.007}},
        'to_interchange': True,
        'full': True
    },}

# add LJ-graphene
lattices['LJ-graphene'] = lattices['graphene'].copy()
lattices['LJ-graphene']['err'] = 0.07

# add AB-graphene
lattices['AB-graphene'] = lattices['LJ-graphene'].copy()

# add AB-uncoupled-graphene
lattices['AB-uncoupled-graphene'] = lattices['LJ-graphene'].copy()

# add ILP-graphene
lattices['ILP-graphene'] = lattices['graphene'].copy()
lattices['ILP-graphene']['potential'] = ['CH.airebo', 'BNCH.ILP']
lattices['ILP-graphene']['full'] = True

# add monolayer twisted graphene
lattices['monolayer-graphene'] = lattices['graphene'].copy()
lattices['monolayer-graphene']['err'] = 0.09
lattices['strained-graphene'] = lattices['graphene'].copy()
lattices['strained-graphene']['err'] = 0.06
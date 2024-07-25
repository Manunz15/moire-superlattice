# Lorenzo Manunza, Università degli Studi di Cagliari, April 2024

lattices = {
    # source: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6116708/ and https://en.wikipedia.org/wiki/Graphite#Structure
    'graphene': {
        'potential': 'CH.airebo',
        'step': 1.42,
        'z_step': 3.35,
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
        'atom_types': {'B': {'id': 1, 'mass': 10.811},
                       'N': {'id': 2, 'mass': 14.007}},
        'to_interchange': True,
        'full': True
    },}

# add LJ-graphene
lattices['LJ-graphene'] = lattices['graphene'].copy()

# add ILP-graphene
lattices['ILP-graphene'] = lattices['graphene'].copy()
lattices['ILP-graphene']['potential'] = ['CH.airebo', 'BNCH.ILP']
lattices['ILP-graphene']['full'] = True

# add monolayer twisted graphene
lattices['monolayer-graphene'] = lattices['graphene'].copy()
lattices['strained-graphene'] = lattices['graphene'].copy()
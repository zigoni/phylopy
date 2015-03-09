def parse_model(model):
    model_parameter = {
        'GTR': ('dirichlet(1,1,1,1)', '6'),
        'HKY': ('dirichlet(1,1,1,1)', '2'),
        'F81': ('dirichlet(1,1,1,1)', '1'),
        'SYM': ('fixed(equal)', '6'),
        'K80': ('fixed(equal)', '2'),
        'JC': ('fixed(equal)', '1'),
    }

    model = model.split('+')
    stem = model[0]
    statefreqpr, nst = model_parameter[stem]
    if len(model) == 2:
        if model[1] == 'G':
            rates = 'gamma'
        else:
            rates = 'propinv'
    elif len(model) == 3:
        rates = 'invgamma'
    else:
        rates = 'equal'
    return statefreqpr, nst, rates
def normalize(lower, upper, vals):
    return [(lower + (upper - lower)*v) for v in vals]

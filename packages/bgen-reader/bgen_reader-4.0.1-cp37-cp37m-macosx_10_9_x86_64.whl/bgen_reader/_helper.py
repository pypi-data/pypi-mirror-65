def get_genotypes(ploidy, nalleles):
    g = [_make_genotype(p, 1, nalleles) for p in ploidy]
    g = sorted([list(reversed(i)) for i in g])
    g = [list(reversed(i)) for i in g]
    return g


def genotypes_to_allele_counts(genotypes):
    nalleles = genotypes[-1][0]
    counts = []
    for g in genotypes:
        count = [0] * nalleles
        for gi in g:
            count[gi - 1] += 1
        counts.append(count)
    return counts


def _make_genotype(ploidy, start, end):
    tups = []
    if ploidy == 0:
        return tups
    if ploidy == 1:
        return [[i] for i in range(start, end + 1)]
    for i in range(start, end + 1):
        t = _make_genotype(ploidy - 1, i, end)
        for ti in t:
            tups += [[i] + ti]
    return tups

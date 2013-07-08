#!/usr/bin/env python
import itertools
import random


def choo(n, iterable):
    ii = iter(iterable)
    while True:
        a = tuple(itertools.islice(ii, n))
        if len(a) < n:
            return
        else:
            yield a
            ii = itertools.chain(a[1:], ii)


wrap = lambda ll: ((i[:-1], i[-1]) for i in ll)


def ll_merge2dict(ll, update_fn, new_fn):
    o = {}
    for i in ll:
        if i[0] in o:
            o[i[0]] = update_fn(o[i[0]], i[1])
        else:
            o[i[0]] = new_fn(i[1])
    return o


def generate(chain):
    oos = random.choice(chain.keys())
    while True:
        if oos not in chain:
            oos = random.choice(chain.keys())
        nu = random.choice(chain[oos])
        yield nu
        oos = tuple(oos[1:] + (nu,))


comb_n_gen = lambda n, combine_fn, gen: combine_fn(itertools.islice(gen(), n))



mkchain = lambda n, it: ll_merge2dict(wrap(choo(n, it)), lambda o, n: tuple(o + (n,)), lambda a: (a,))
gettext = lambda n, chain, combine_fn=None: comb_n_gen(gen=lambda: generate(chain), combine_fn=(''.join if (combine_fn is None) else combine_fn), n=n)





if __name__ == '__main__':
    import sys


    if (len(sys.argv) > 1) and (sys.argv[1] == '--help'):
        'Takes text on stdin, level as param 1, amount of items to generate as param 2, "char" to work on chars as units instead of words as optional param 3 '
    else:
        ft = sys.stdin.read()
        chars = ((len(sys.argv) > 3) and sys.argv[3] == 'char')
        items = (ft if chars else ft.split())
        sys.stdout.write(''.join((comb_n_gen(gen=lambda: generate(ll_merge2dict(wrap(choo(int(sys.argv[1]), items)), lambda o, n: tuple(set(o + (n,))), lambda a: (a,))), combine_fn=('' if chars else ' ').join, n=int(sys.argv[2])), "\n")))

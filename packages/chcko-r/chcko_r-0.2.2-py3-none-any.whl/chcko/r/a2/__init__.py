from chcko.chcko.hlp import Struct
import random
from sympy import Integer
from itertools import product
from numpy import where
is_natural = lambda x: x.is_integer and x>=0
rch = random.choice
def given():
    g = Struct()
    random.seed()
    g.a = Integer(rch([-1,1]))
    op = '+-*/'
    opnd = product(op,['ab','ba'])
    ops = [o[0].join(o[1]) for o in opnd]
    random.shuffle(ops)
    takeop= lambda s: next(x for x in ops if s in x)
    g.ops = [takeop(s) for s in op]
    random.shuffle(g.ops)
    g.rep = ['b',f"{rch('+-')}{rch('23')}*a"]
    return g
def calc(g):
    #g=given()
    res1 = [is_natural(eval(x.replace(*g.rep),{**g})) for x in g.ops]
    res = [''.join([chr(65+x) for x in where(res1)[0]])]
    return res

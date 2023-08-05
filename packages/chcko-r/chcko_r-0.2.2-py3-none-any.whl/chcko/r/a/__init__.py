import random
import math as m
from chcko.chcko.hlp import Struct
def angle_deg(i, g):
    d = dict(zip('abc', ([g.a, g.b, g.c]*2)[i:]))
    return eval('180*acos((a*a+b*b-c*c)/2/a/b)/pi', {**d,'acos':m.acos,'pi':m.pi})
def given():
    random.seed()
    a, b = random.sample(range(1, 10), 2)
    c = random.randrange(max(a - b + 1, b - a + 1), a + b)
    return Struct(a=a, b=b, c=c)
def calc(g):
    return [angle_deg(i, g) for i in range(3)]
chames = [r'\(\alpha=\)', r'\(\beta=\)', r'\(\gamma=\)']

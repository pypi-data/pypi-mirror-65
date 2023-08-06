from chcko.chcko.hlp import Struct
import numpy as np
import pint
u = pint.UnitRegistry()
import random

def given():
    g = Struct()
    g.Vcc = random.choice(range(7,15))*u.V
    g.Vi = random.choice(range(4,g.Vcc.magnitude-2))*u.V
    g.hfe = random.choice(range(5,15))*10
    g.Vbe = random.choice([0.3,0.7])*u.V
    g.Rc = (random.choice(range(100))+100)*10*u.ohm
    Vo1 = random.choice(range(2,g.Vi.magnitude-1))*u.V
    ReRL = g.Rc/(g.Vcc/Vo1-1)
    g.RL = g.Re = 2*round(ReRL.magnitude)*u.ohm
    return g
def calc(g):
    #g = given()
    Vo0 = g.RL/(g.RL+g.Rc)*g.Vcc
    Vo1 = g.Vcc*(1-g.Rc/(g.Rc+1/(1/g.Re+1/g.RL)))
    g.Icmax = Vo1/g.Re
    Ibmax = g.Icmax/g.hfe
    Rb = (g.Vi-Vo1-g.Vbe)/Ibmax
    res = [x.to('V').magnitude for x in [Vo0,Vo1]] + [Rb.to('kΩ').magnitude]
    return res
chames = [r'\(V_0/V=\)', r'\(V_1/V=\)', r'\(R_b/kΩ=\)']
P = lambda x: "{:~P}".format(x)


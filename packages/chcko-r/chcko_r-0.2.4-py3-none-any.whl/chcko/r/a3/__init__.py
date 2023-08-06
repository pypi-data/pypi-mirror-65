from chcko.chcko.hlp import Struct
import numpy as np
import pint
u = pint.UnitRegistry()
import random
def given():
    g = Struct()
    g.Vcc = random.choice(range(7,15))*u.V
    g.Vi = random.choice(range(4,g.Vcc.magnitude-2))*u.V
    g.Vo = random.choice(range(1,g.Vi.magnitude))*u.V
    g.hfe = random.choice(range(5,15))*10
    g.Icmax = random.choice(range(5,15))*u.mA
    g.Vbe = random.choice([0.3,0.7])*u.V
    return g
def calc(g):
    #g = given()
    VceCutoff = g.Vcc
    VceSaturation = 0
    ReRc = (g.Vcc-VceSaturation)/g.Icmax
    #Rc = (g.Vcc/g.Vo-1)*Re
    Re = ReRc*g.Vo/g.Vcc
    Rc = ReRc - Re
    Ibmax = g.Icmax/g.hfe
    Rb = (g.Vi-g.Vo-g.Vbe)/Ibmax
    res = [x.to('kΩ').magnitude for x in [Rc,Re,Rb]]
    return res
chames = [r'\(R_c/kΩ=\)', r'\(R_e/kΩ=\)', r'\(R_b/kΩ=\)']
P = lambda x: "{:~P}".format(x)


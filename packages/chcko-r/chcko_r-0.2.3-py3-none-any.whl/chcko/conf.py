
try:
    from chcko.chcko import conf
except ModuleNotFoundError:
    import sys
    import os.path as p
    chckoparallel = p.normpath(p.join(p.dirname(__file__),'..','..','chcko'))
    sys.path.insert(0,chckoparallel)
    from chcko.chcko import conf


globals().update({k:v for k,v in conf.__dict__.items() if not k.startswith('__')})


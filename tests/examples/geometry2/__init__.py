from .modules import circle
from .modules import cylinder

def load_modules(mm):
    mm.add_module("Circle", circle.Circle())
    mm.add_module("Cylinder", cylinder.Cylinder())

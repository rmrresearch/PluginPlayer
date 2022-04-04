from .modules import circle

def load_modules(mm):
    mm.add_module("Area of a circle", circle.Circle())

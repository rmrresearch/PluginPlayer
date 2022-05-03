import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname('tests'))

from tests.examples.geometry2.modules import circle
from tests.examples.geometry2.modules import cylinder

def load_modules(mm):
    mm.add_module("Circle", circle.Circle())
    mm.add_module("Cylinder", cylinder.Cylinder())

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname('tests'))

from tests.examples.geometry.modules import area
from tests.examples.geometry.modules import prism_volume

def load_modules(mm):
        mm.add_module("Area of a triangle", area.Triangle())
        mm.add_module("Area of a square", area.Square())
        mm.add_module("Area of a rectangle", area.Rectangle())
        mm.add_module("Volume of a prism", prism_volume.PrismVolumeBySubmod())


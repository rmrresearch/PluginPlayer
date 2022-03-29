from .property_types.area import Area
from .property_types.prism_volume import PrismVolume
from .modules import area
from .modules import prism_volume

def load_modules(mm):
    mm.add_module("Area of a triangle", area.Triangle())
    mm.add_module("Area of a square", area.Square())
    mm.add_module("Area of a rectangle", area.Rectangle())
    mm.add_module("Volume of a prism", prism_volume.PrismVolumeBySubmod())
    mod_key = 'Volume of a prism'
    mm.change_submod(mod_key, 'area', 'Area of a triangle')

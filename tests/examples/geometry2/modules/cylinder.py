import pluginplay as pp
from ...geometry.property_types.area import Area
from ...geometry.property_types.areacircle import AreaCircle
from ...geometry.property_types.cylinder_volume import CylinderVolume
from ...geometry2.modules.circle import Circle
import math

class Cylinder(pp.Module):

    def __init__(self):

        def fxn(inputs, submods):
            area = submods[('circleArea', AreaCircle())].run_as(AreaCircle(), inputs['radius'])
            return {'volume' : area * inputs['height']}

        super().__init__(property_types=set([CylinderVolume()]),
                        submods={('circleArea', AreaCircle()) : Circle()},
                        callback=fxn,
                        callback_name='Cylinder')

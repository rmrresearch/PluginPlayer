import pluginplay as pp
from ...geometry.property_types.perimetercircle import PerimeterCircle
from ...geometry.property_types.areacircle import AreaCircle
import math

class Circle(pp.Module):

    def __init__(self):

        def fxn(inputs, _):
            perimeter =  2 * inputs['radius'] * inputs['pi']
            area = inputs['radius'] * inputs['radius'] * inputs['pi']
            return {'area' : area,'perimeter' : perimeter}

        super().__init__(property_types=set([AreaCircle(), PerimeterCircle()]),
                         inputs={"pi" : math.pi},
                         callback=fxn,
                         callback_name='Circle')

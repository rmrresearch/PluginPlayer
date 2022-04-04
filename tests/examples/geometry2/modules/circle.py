import pluginplay as pp
from ...geometry.property_types.area import Area
import math

class Circle(pp.Module):

    def __init__(self):

        def fxn(inputs, _):
            if inputs['base'] != inputs['height']:
                raise ValueError("Expected base == height b/c I'm too lazy to "
                                 "define a better area property type")

            area = inputs['base'] * inputs['base'] * inputs['pi']
            return {'area' : area}

        super().__init__(property_types=set([Area()]),
                         inputs={"pi" : math.pi},
                         callback=fxn,
                         callback_name='Circle')

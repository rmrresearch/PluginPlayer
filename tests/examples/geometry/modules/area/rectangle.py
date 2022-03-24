import pluginplay as pp
from ...property_types.area import Area

class Rectangle(pp.Module):

    def __init__(self):

        def fxn(inputs, _):
            area = inputs['base'] * inputs['height']
            return {'area' : area}

        super().__init__(property_types=set([Area()]),
                         callback= fxn,
                         callback_name='Rectangle')

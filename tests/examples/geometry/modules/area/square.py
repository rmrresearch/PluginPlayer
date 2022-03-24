import pluginplay as pp
from ...property_types.area import Area

class Square(pp.Module):

    def __init__(self):

        def fxn(inputs, _):
            if inputs['base'] != inputs['height']:
                raise ValueError("Expected base == height")

            area = inputs['base'] ** 2
            return {'area' : area}

        super().__init__(property_types=set([Area()]),
                         callback= fxn,
                         callback_name='Square')

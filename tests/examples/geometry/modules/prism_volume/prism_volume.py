import pluginplay as pp
from ...property_types.area import Area
from ...property_types.prism_volume import PrismVolume

class PrismVolumeBySubmod(pp.Module):

    def __init__(self):
        def fxn(inputs, submods):
            b, h, w = PrismVolume().unwrap_inputs(inputs)
            area = submods[('area', Area())].run_as(Area(), b, h)
            return {'volume' : area * w}

        super().__init__(property_types=set([PrismVolume()]),
                         callback= fxn,
                         callback_name='PrismVolumeBySubmod',
                         submods={('area', Area()) : None},
                         description="Computes the volume of a prism")

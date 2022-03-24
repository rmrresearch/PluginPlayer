import pluginplay as pp

class PrismVolume(pp.PropertyType):

    def __init__(self):
        inputs = [('base', None), ('height', None), ('width', None)]
        results = ['volume']
        return super().__init__(inputs, results)

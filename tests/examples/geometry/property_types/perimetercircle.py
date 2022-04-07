import pluginplay as pp
class PerimeterCircle(pp.PropertyType):

    def __init__(self):
        inputs = [('radius', None)]
        results = ['perimeter']
        return super().__init__(inputs, results)

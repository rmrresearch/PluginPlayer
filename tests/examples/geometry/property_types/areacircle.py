import pluginplay as pp
class AreaCircle(pp.PropertyType):

    def __init__(self):
        inputs = [('radius', None)]
        results = ['area']
        return super().__init__(inputs, results)

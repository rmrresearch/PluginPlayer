import pluginplay as pp
class Area(pp.PropertyType):

    def __init__(self):
        inputs = [('base', None), ('height', None)]
        results = ['area']
        return super().__init__(inputs, results)

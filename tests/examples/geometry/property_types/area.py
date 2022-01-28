from pluginplayer import property_type

class Area(property_type.PropertyType):

    def __init__(self):
        inputs = [('base', None), ('height', None)]
        results = ['area']
        return super().__init__(inputs, results)

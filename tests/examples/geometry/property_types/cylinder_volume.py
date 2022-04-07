import pluginplay as pp

class CylinderVolume(pp.PropertyType):

    def __init__(self):
        inputs = [('height', None),('radius', None)]
        results = ['volume']
        return super().__init__(inputs, results)

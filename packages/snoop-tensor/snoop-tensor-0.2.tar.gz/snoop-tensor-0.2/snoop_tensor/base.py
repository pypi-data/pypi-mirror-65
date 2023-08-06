class Formatter:
    def __init__(self, disp_name, property_name=False, properties=[]):
        self.properties = properties
        self.properties_name = property_name
        self.disp_name = disp_name

    def __call__(self, tensor):
        prefix = self.disp_name + '<'
        suffix = '>'
        properties_str = ''
        for p in self.properties:
            new = ''
            if self.properties_name:
                new += p + '='
            if hasattr(self, 'repr_' + p):
                new += getattr(self, 'repr_' + p)(tensor)
            else:
                raise ValueError('Unknown tensor property')

            if properties_str != '' and len(new) > 0:
                properties_str += ', '
            properties_str += new

        return prefix + properties_str + suffix

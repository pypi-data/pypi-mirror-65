import numpy

from snoop_tensor.base import Formatter

class TensorFormatter(Formatter):
    def __init__(self, property_name=False, properties=('shape', 'dtype', 'has_nan', 'has_inf')):
        super().__init__("ndarray", property_name, properties)

    def repr_shape(self, array):
        return str(array.shape)

    def repr_dtype(self, array):
        return str(array.dtype)

    def repr_has_nan(self, array):
        result = bool(numpy.isnan(array).any())
        if self.properties_name:
            return str(result)
        if result:
            return 'has_nan'
        return ''

    def repr_has_inf(self, tensor):
        result = bool(numpy.isinf(tensor).any())
        if self.properties_name:
            return str(result)
        if result:
            return 'has_inf'
        return ''

import torch

from snoop_tensor.base import Formatter


class TensorFormatter(Formatter):
    FLOATING_POINTS = ['float', 'double', 'half', 'complex128', 'complex32', 'complex64']

    def __init__(self, property_name=False, properties=('shape', 'dtype', 'device', 'requires_grad', 'has_nan', 'has_inf')):
        super().__init__("tensor", property_name, properties)

    def repr_shape(self, tensor):
        ret = ''
        if not hasattr(tensor, 'names') or not tensor.has_names():
            ret += str(tuple(tensor.shape))
        else:
            ret += '('
            for n, v in zip(tensor.names, tensor.shape):
                if n is not None:
                    ret += '{}={}, '.format(n, v)
                else:
                    ret += '{}, '.format(v)
            ret = ret[:-2] + ')'
        return ret

    def repr_dtype(self, tensor):
        dtype_str = str(tensor.dtype)
        dtype_str = dtype_str[len('torch.'):]
        return dtype_str

    def repr_device(self, tensor):
        return str(tensor.device)

    def repr_requires_grad(self, tensor):
        if self.properties_name:
            return str(tensor.requires_grad)
        if tensor.requires_grad:
            return 'grad'
        return ''

    def repr_has_nan(self, tensor):
        result = tensor.dtype in TensorFormatter.FLOATING_POINTS and bool(torch.isnan(tensor).any())
        if self.properties_name:
            return str(result)
        if result:
            return 'has_nan'
        return ''

    def repr_has_inf(self, tensor):
        result = tensor.dtype in TensorFormatter.FLOATING_POINTS and bool(torch.isinf(tensor).any())
        if self.properties_name:
            return str(result)
        if result:
            return 'has_inf'
        return ''

class LayerFormatter:
    def __init__(self):
        pass

    def __call__(self, layer):
        return type(layer).__name__

import snoop
import cheap_repr
import snoop.configuration

def register(verbose=False,
    torch_formatter=None, numpy_formatter=None,
    report_gpu_mem=False, report_time_cost=False
):
    try:
        import numpy
        from snoop_tensor.numpy import TensorFormatter
        numpy_formatter = numpy_formatter or TensorFormatter()
        cheap_repr.register_repr(numpy.ndarray)(lambda x, _: numpy_formatter(x))
    except ImportError:
        pass

    try:
        import torch
        from snoop_tensor.torch import TensorFormatter, LayerFormatter
        torch_formatter = torch_formatter or TensorFormatter()
        torch_layer_formatter = LayerFormatter()
        cheap_repr.register_repr(torch.Tensor)(lambda x, _: torch_formatter(x))
        cheap_repr.register_repr(torch.nn.Module)(lambda x, _: torch_layer_formatter(x))
    except ImportError:
        pass

    if report_gpu_mem:
        from snoop_tensor.profiler import GPUMemoryWatcher
        snoop.config.watch_extras += (GPUMemoryWatcher.create_watcher(report_gpu_mem),)
    if report_time_cost:
        from snoop_tensor.profiler import TimeCostWatcher
        snoop.config.watch_extras += (TimeCostWatcher.create_watcher(),)

    unwanted = {
        snoop.configuration.len_shape_watch,
        snoop.configuration.dtype_watch,
    }
    snoop.config.watch_extras = tuple(x for x in snoop.config.watch_extras if x not in unwanted)

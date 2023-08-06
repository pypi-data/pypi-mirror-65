import os
import time

class GPUMemoryWatcher:
    def __init__(self, gpus=None):
        from py3nvml import py3nvml
        py3nvml.nvmlInit()

        self.gpus = gpus or range(py3nvml.nvmlDeviceGetCount())

    def __call__(self, source, value):
        from py3nvml import py3nvml

        try:
            ret = []
            for gidx in self.gpus:
                handle = py3nvml.nvmlDeviceGetHandleByIndex(gidx)
                procs = py3nvml.nvmlDeviceGetComputeRunningProcesses(handle)
                try:
                    cproc = next(p for p in procs if p.pid == os.getpid())
                except StopIteration:
                    continue
                usage = self._print_size(cproc.usedGpuMemory)
                ret.append("{}: {}".format(gidx, usage))

            if len(ret) == 0:
                return 'gpu_mem', 'unused'
            else:
                return 'gpu_mem', ', '.join(ret)
        except:
            print("ERROR")
            import sys
            e = sys.exc_info()[0]
            return 'gpu_mem', str(e)

    def _print_size(self, size):
        suffix = ['B', 'KB', 'MB', 'GB']
        level = 0
        size = float(size)
        while size > 1024:
            size /= 1024
            level += 1
        return "%.2f%s" % (size, suffix[level])

    @staticmethod
    def create_watcher(*args):
        watcher = GPUMemoryWatcher(*args)
        return lambda source, value: watcher(source, value)

class TimeCostWatcher:
    def __init__(self):
        self.last_time = time.time()

    def __call__(self, source, value):
        new_time = time.time()
        duration = new_time - self.last_time
        self.last_time = new_time

        return 'time elapsed', "%.4fs" % duration

    @staticmethod
    def create_watcher(*args):
        watcher = TimeCostWatcher(*args)
        return lambda source, value: watcher(source, value)

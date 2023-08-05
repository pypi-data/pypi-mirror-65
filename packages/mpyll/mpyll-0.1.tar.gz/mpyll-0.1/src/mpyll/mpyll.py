import multiprocessing as mp
import random
import math
from inspect import isfunction

class Parallelizer(object):

    def __init__(self, task, post_processor = None, n_jobs = -1):
        # check arguments
        if not isfunction(task):
            raise ValueError('task argument is not a callable')
        if post_processor is not None and not isfunction(post_processor):
            raise ValueError('post_processor argument is not a callable')
        if not isinstance(n_jobs, int) or n_jobs == 0:
            raise ValueError('invalid n_jobs value')
        # constructor objects
        self._task = task
        self._post_processor = post_processor
        cpu_threads = mp.cpu_count()
        if n_jobs < 0 or n_jobs > cpu_threads:
            self._n_jobs = cpu_threads
        else:
            self._n_jobs = n_jobs

    def _initialize(self):
        self._task_args = list()
        self._task_kwargs = dict()
        self._post_processor_args = list()
        self._post_processor_kwargs = dict()
        self._manager = mp.Manager()
        self._shared_memory = None

    def _parse_arguments(self, args, kwargs):
        if args is not None:
            for e in args:
                if e.startswith(self._task.__name__ + '_'):
                    arg = e.replace(self._task.__name__ + '_', '')
                    self._task_args.append(arg)
                if e.startswith(self._post_processor.__name__ + '_'):
                    arg = e.replace(self._post_processor.__name__ + '_', '')
                    self._post_processor_args.append(arg)
        if kwargs is not None:
            for k, v in kwargs.items():
                if k.startswith(self._task.__name__ + '_'):
                    arg = k.replace(self._task.__name__ + '_', '')
                    self._task_kwargs[arg] = v
                if k.startswith(self._post_processor.__name__ + '_'):
                    arg = k.replace(self._post_processor.__name__ + '_', '')
                    self._post_processor_kwargs[arg] = v

    def _split_data(self, data, shuffle = False):
        if shuffle:
            random.shuffle(data)
        q = math.floor(len(data) / self._n_jobs)
        sizes = [q for _ in range(self._n_jobs)]
        for i in range(len(data) % self._n_jobs):
            sizes[i] += 1
        sizes = [size for size in sizes if size != 0]
        data_chunks = list()
        i = 0
        for size in sizes:
            data_chunks.append(data[i:i + size])
            i += size
        return data_chunks
    
    def _target_wrapper(self, data):
        rv = self._task(data, *self._task_args, **self._task_kwargs)
        self._shared_memory.append(rv)

    def _post_process(self):
        if self._post_processor is None:
            rv = list(self._shared_memory)
        else:
            rv = self._post_processor(self._shared_memory,
                                      *self._post_processor_args, 
                                      **self._post_processor_kwargs)
        return rv
    
    def run(self, data, shuffle_data = False, *args, **kwargs):
        # check arguments
        if not isinstance(data, list):
            raise ValueError('Invalid data argument: expecting a list')
        if not isinstance(shuffle_data, bool):
            raise ValueError('Invalid shuffle_data value: expecting a boolean')
        # init
        self._initialize()
        # parse args and kwargs
        self._parse_arguments(args, kwargs)
        # initialize the shared memory
        self._shared_memory = self._manager.list()
        # split data
        data_chunks = self._split_data(data, shuffle_data)
        # execute jobs
        processes = list()
        for data_chunk in data_chunks:
            process = mp.Process(target = self._target_wrapper, 
                                 args = (data_chunk,), kwargs = {})
            processes.append(process)
        for process in processes:
            process.start()
        for process in processes:
            process.join()
        # post processing
        return self._post_process()

def parallelize(task, 
                data, 
                shuffle_data = False, 
                post_processor = None, 
                n_jobs = -1, 
                *args, **kwargs):
    ll = Parallelizer(task, post_processor = post_processor, n_jobs = n_jobs)
    return ll.run(data, shuffle_data = shuffle_data, *args, **kwargs)

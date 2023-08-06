from collections import Mapping
from contextlib import contextmanager
import cProfile, pstats, io

import yaml

def load_yaml_file(filename):
    with open(filename,'r') as readfile:
        data = readfile.read()
        return yaml.safe_load(data)
    

@contextmanager
def profiling(output_filename):
    pr = cProfile.Profile()
    pr.enable()
    try:
        yield
    finally:
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        with open(output_filename, 'w+') as profile_stream:
            ps = pstats.Stats(pr, stream=profile_stream).sort_stats(sortby)
            ps.print_stats()

class GetRecursiveMixin(object):
    
    def get_recursive(self, as_str=None, as_array=None):
        if as_str:
            as_array = as_str.split('.')
        
        this_attr_name, *as_array = as_array
        this_attr = self._get_attr_recursive(this_attr_name)
        

        if as_array:
            if not isinstance(this_attr, GetRecursiveMixin):
                this_attr = AnonymousGetRecursive(this_attr)
            return this_attr.get_recursive(as_array=as_array)
        else:
            return this_attr
    
    def _get_attr_recursive(self, name):
        return getattr(self, name)

class GetRecursiveKeyMixin(GetRecursiveMixin):

    def _get_attr_recursive(self, name):
        return self[name]

class AnonymousGetRecursive(GetRecursiveMixin):
    def __init__(self, obj):
        self.obj = obj

    def _get_attr_recursive(self, name):
        if isinstance(self.obj, Mapping):
            return self.obj[name]
        else:
            return getattr(self.obj, name)


from dateutil.tz import tzlocal

from collections.abc import Mapping
from contextlib import contextmanager
import cProfile, pstats, io

import yaml

try:
    import numpy as np
    isnan = np.isnan
except ImportError:
    isnan = lambda x: x is None


def load_yaml_file(filename):
    with open(filename,'r') as readfile:
        data = readfile.read()
        return yaml.safe_load(data)
    
def write_yaml_file(filename, content):
    with open(filename,'w+') as writefile:
        yaml.dump(content, writefile)

def local_tz():
    return tzlocal()

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

from collections.abc import Mapping
from itertools import chain, starmap

class DefaultValue(object):
    def __init__(self, value_or_fn):
        self.value_or_fn = value_or_fn

    def resolve(self):
        if callable(self.value_or_fn):
            return self.value_or_fn()
        else:
            return self.value_or_fn

DEFAULT_PLACEHOLDER = DefaultValue(None)

def update(target, updater):
    """Deep update of dict target using updater. 
    
    The special DEFAULT_PLACEHOLDER object allows to set default values"""
    for key, value in updater.items():
        if isinstance(value, Mapping):
            target[key] = update(target.get(key, {}), value)
        else:
            if is_default(value) and key in target:
                # Do no replace existing value with the default placeholder
                pass
            else:
                target[key] = value
    return target

def is_default(value):
    return isinstance(value, DefaultValue)

def replace_defaults(target):
    for key, value in target.items():
        if isinstance(value, Mapping):
            replace_defaults(value)
        else:
            if is_default(value):
                target[key] = value.resolve()
    return target

def deepen_value_in_dict(key_prefix, value):
    result = {}
    next_dict = result
    for key in key_prefix[:-1]:
        next_dict[key] = {}
        next_dict = next_dict[key]
    next_dict[key_prefix[-1]] = value
    
    return result

def deepen_dict(flat_dict):
    result = {}
    for key, value in flat_dict.items():
        update(result, deepen_value_in_dict(key, value))
    return result

def flatten_dict(dictionary):
    """Flatten a nested dictionary structure"""

    tuplify = lambda key: key if isinstance(key, tuple) else (key,)

    def unpack(parent_key, parent_value):
        """Unpack one level of nesting in a dictionary"""
        try:
            items = parent_value.items()
        except AttributeError:
            # parent_value was not a dict, no need to flatten
            yield (parent_key, parent_value)
        else:
            for key, value in items:
                yield (parent_key + tuplify(key), value)


    # Put each key into a tuple to initiate building a tuple of subkeys
    dictionary = {tuplify(key): value for key, value in dictionary.items()}

    while True:
        # Keep unpacking the dictionary until all value's are not dictionary's
        dictionary = dict(chain.from_iterable(starmap(unpack, dictionary.items())))
        if not any(isinstance(value, dict) for value in dictionary.values()):
            break

    return dictionary
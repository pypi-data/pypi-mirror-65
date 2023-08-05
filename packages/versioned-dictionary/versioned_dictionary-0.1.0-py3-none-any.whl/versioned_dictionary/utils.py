import hashlib
import json
import binascii
from collections import MutableMapping
import pandas as pd
import numpy as np

def flatten(d, parent_key='', sep='.'):
    """
    This function returns a flattened nested dictionary, e.g.,

    >> d = {'a':1, 'b':{'c':3,'d':4}}
    >> flatten(d)
    >> {'a': 1, 'b_c': 3, 'b_d': 4}
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def unflatten(dictionary, sep='.'):
    """
    This function returns a nested dictionary from a flattened one,

    >> e = {'a': 1, 'b_c': 3, 'b_d': 4}
    >> unflatten(e)
    >> {'a': 1, 'b': {'c': 3, 'd': 4}}
    """
    resultDict = dict()
    for key, value in dictionary.items():
        parts = key.split(sep)
        d = resultDict
        for part in parts[:-1]:
            if part not in d:
                d[part] = dict()
            d = d[part]
        d[parts[-1]] = value
    return resultDict

def hasher(x):
    return hashlib.sha224((json.dumps(x)).encode('utf-8')).hexdigest()

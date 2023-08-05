import json
import json_tricks
# from .utils import hasher, JSONEncoder
import python_jwt as jwt
import datetime
from collections import namedtuple
import hashlib
import binascii
import pandas as pd
from collections import MutableMapping

# --- Definitions ---

from json import JSONEncoder
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def hasher(x):
    if isinstance(x,dict):
        f = flatten(x)
        L = sorted(flatten(x).items(), key=lambda kv:kv[0])
        x = unflatten({x[0]:x[1] for x in L})
    return hashlib.sha224((json.dumps(x, cls=MyEncoder)).encode('utf-8')).hexdigest()

def flatten(d, parent_key='', sep='.'):
    """
    This function returns a flattened nested dictionary, e.g.,

    >> d = {'a':1, 'b':{'c':3,'d':4}}
    >> flatten(d)
    >> {'a': 1, 'b_c': 3, 'b_d': 4}
    """
    if isinstance(d, MutableMapping):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, MutableMapping):
                items.extend(flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    if isinstance(d, VersionedDict):
        parent_key = d.name
        items = []
        for k, v in d.root_object.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, (MutableMapping,VersionedDict)):
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

class Change(object):
    allowed_verbs = ['add', 'set', 'del']
    def __init__(self, VersionedDict_root_hash, state, verb, key, to):
        self.VersionedDict_root_hash = VersionedDict_root_hash
        self.state = state
        self.verb = verb
        self.key = key
        self.to = to
        self.hash = hasher(json.dumps([self.VersionedDict_root_hash, state, verb, key, to]))
        self.old_value = None
        self.has_been_applied = False
        self.end_state = None
        self.application_time = None

    def __neg__(self):
        if self.verb=='set':
            return Change(self.VersionedDict_root_hash, self.end_state, 'set', self.key, self.old_value)
        if self.verb=='add':
            return Change(self.VersionedDict_root_hash, self.end_state, 'del', self.key, self.old_value)
        if self.verb=='del':
            return Change(self.VersionedDict_root_hash, self.end_state, 'add', self.key, self.old_value)

    def __str__(self):
        s = []
        s.append(80*'-')
        s.append("=== CHANGE ===")
        s.append("hash         : {0}".format(self.hash))
        s.append("VersionedDict hash : {0}".format(self.VersionedDict_root_hash))
        s.append("state        : {0}".format(self.state))
        s.append("verb         : {0}".format(self.verb))
        s.append("key          : {0}".format(self.key))
        s.append("to           : {0}".format(self.to))
        s.append("applied      : {0}".format(self.has_been_applied))
        s.append("time         : {0}".format(self.application_time))
        s.append("old_value    : {0}".format(self.old_value))
        s.append("end_state    : {0}".format(self.end_state))
        s.append(80*'-')
        return "\n".join(s)

class VersionedDict():
    def __init__(self, name='', root_object={}):
        self.name = name
        self.root_object = root_object
        self.creation_time = datetime.datetime.now().isoformat()
        self.last_modified = None
        self.changes = []
        self.states_history = [hasher(self.root_object)]
        self.changetime_history = [self.creation_time]
        self.root_hash = self.states_history[0]

    @staticmethod
    def from_json(data):
        return json_tricks.loads(data)

    def __len__(self):
        return len(self.root_object)

    def to_json(self):
        return json_tricks.dumps(self)

    def current_state(self):
        return self.states_history[-1]

    def __getitem__(self, key):
        _f = flatten(self)
        if isinstance(_f,dict):
            res = _f.__getitem__(key)
        return res

    def reset(self):
        self.states_history = self.states_history[-1:]
        self.changetime_history = self.changetime_history[-1:]
        self.root_hash = self.states_history[0]
        self.last_modified = None

    def apply_change(self, change):
        change.application_time = datetime.datetime.now().isoformat()
        self.last_modified = change.application_time
        if not isinstance(change, Change):
            raise ValueError('Invalid change sequence')
            raise
        if not change.VersionedDict_root_hash==self.root_hash:
            raise ValueError('This change does not belong to this VersionedDict.')
        if not change.verb in change.allowed_verbs:
            raise ValueError("{0}".format(json.dumps(change.allowed_verbs)))
        try:
            assert change.state in self.states_history
        except:
            msg = 'The state associated with the proposed change cannot be found in this VersionedDict'
            raise RuntimeError(msg)

        _f = flatten(self.root_object)

        if change.verb=='set':
            change.old_value = _f.__getitem__(change.key)
            _f.__setitem__(change.key, change.to)

        if change.verb=='add':
            # print("add method {0} {1}".format(change.key, change.to))
            _f.update({change.key: change.to})

        if change.verb=='del':
            change.old_value = _f.__getitem__(change.key)
            _f.pop(change.key)

        self.root_object = unflatten(_f)
        self.states_history.append(hasher(self.root_object))
        self.changetime_history.append(change.application_time)
        change.has_been_applied = True
        change.end_state = self.states_history[-1]
        self.changes.append(change)

    def history(self):
        print("=== History ===")
        change_hashes = ['']+[x.hash for x in self.changes]
        verbs = ['']+[x.verb for x in self.changes]
        keys = ['']+[x.key for x in self.changes]
        old_values = ['']+[x.old_value for x in self.changes]
        tos = ['']+[x.to for x in self.changes]
        Z = [
           self.changetime_history,
           self.states_history,
           verbs,
           keys,
           old_values,
           tos,
           change_hashes]
        cols = ['time', 'state', 'verb', 'key', 'old', 'new', 'hash change']
        df = pd.DataFrame(list(map(list, zip(*Z))), columns = cols)
        return df

    def revert_to_state(self, state):
        """
        we use this function to revert the VersionedDict object to a certain state if
        obviously, this state existed in the past. In order to do that, we will
        have to walk back and reverse the changes at every step.
        """
        if state in self.states_history:
            L = list(reversed(self.changes))
            for change in L:
                change.application_time = datetime.datetime.now().isoformat()
                self.apply_change(-change)
                if self.current_state() == state:
                    break

    def undo(self, steps=1):
        try:
            self.revert_to_state(self.states_history[-(1+steps)])
        except IndexError:
            print('Nothing to undo')

    def print_changes(self):
        s = []
        s.append("changes")
        for x in self.changes:
            s.append(x.__str__())
        s.append(80*'-')
        print( "\n".join(s))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = []
        s.append(80*'-')
        s.append("=== VersionedDict ===")
        s.append("name         : {0}".format(self.name))
        # s.append("dict         : {0}".format(json.dumps(self.root_object, cls=JSONEncoder)))
        s.append("root         : {0}".format(self.root_hash))
        s.append("state        : {0}".format(self.current_state()))
        s.append("creation time: {0}".format(self.creation_time))
        s.append("last modified: {0}".format(self.last_modified))
        return "\n".join(s)

if __name__ == '__main__':
    pass

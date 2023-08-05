import json
import json_tricks
from .utils import flatten, unflatten, hasher
import python_jwt as jwt
import datetime
from collections import namedtuple
# --- Definitions ---

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

class VersionedDict(object):
    @staticmethod
    def from_json(data):
        return json_tricks.loads(data)

    @staticmethod
    def load(filename, key=None):
        if not key:
            return json_tricks.load(filename)
        else:
            emsg = open(filename,'r').readlines()[0][1:-1]
            header, claims = jwt.verify_jwt(emsg, key, ['PS256'])
            return json_tricks.loads(json.dumps(claims))

    def to_json(self):
        return json_tricks.dumps(self)

    def __init__(self, name, root_object):
        self.name = name
        self.root_object = root_object
        self.creation_time = datetime.datetime.now()
        self.last_modified = None
        self.changes = []
        self.states_history = [hasher(self.root_object)]
        self.root_hash = self.states_history[0]

    def current_state(self):
        return self.states_history[-1]

    def __getitem__(self, key):
        _f = flatten(self.root_object)
        return _f.__getitem__(key)

    def apply_change(self, change):
        change.application_time = datetime.datetime.now()
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
        change.has_been_applied = True
        change.end_state = self.states_history[-1]
        self.changes.append(change)

    def revert_to_state(self, state):
        """
        we use this function to revert the VersionedDict object to a certain state if
        obviously, this state existed in the past. In order to do that, we will
        have to walk back and reverse the changes at every step.
        """
        if state in self.states_history:
            L = list(reversed(self.changes))
            for c in L:
                self.apply_change(-c)
                if self.current_state() == state:
                    break

    def save(self, filename, key=None):
        """
        In this function we send the serialized version of the VersionedDict object
        to the redis database.
        """
        if not key:
            return json_tricks.dump(self, filename)
        else:
            payload = json.loads(json_tricks.dumps(self))
            token = jwt.generate_jwt(payload, key, 'PS256', datetime.timedelta(minutes=5))
            return json_tricks.dump(token, filename)

    def print_changes(self):
        s = []
        s.append("changes")
        for x in self.changes:
            s.append(x.__str__())
        s.append(80*'-')
        print( "\n".join(s))

    def __str__(self):
        s = []
        s.append(80*'-')
        s.append("=== VersionedDict ===")
        s.append("name         : {0}".format(self.name))
        s.append("dict         : {0}".format(json.dumps(self.root_object)))
        s.append("root         : {0}".format(self.root_hash))
        s.append("state        : {0}".format(self.current_state()))
        s.append("creation time: {0}".format(self.creation_time))
        s.append("last modified: {0}".format(self.last_modified))
        return "\n".join(s)

if __name__ == '__main__':
    C = {"make":"new_class", "name": "N"}
    T = VersionedDict(name='class_N', root_object=C)
    pass

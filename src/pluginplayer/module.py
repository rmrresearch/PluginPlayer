from copy import deepcopy


class Module:
    def __init__(self):
        self._unlocked = True
        self._description = None

    def unlocked_copy(self):
        rv = deepcopy(self)
        rv._unlocked = True
        return rv

    def has_description(self):
        return self._description != None

    def locked(self):
        return not self._unlocked

    def ready(self, prop_type):
        return True

    def list_not_ready(self):
        pass

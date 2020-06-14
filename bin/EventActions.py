# Used to add functions that might otherwise be chat commands, but are run on events instead.
# Added to separate file to allow for hot-reloading of module.
from inspect import getmembers, isfunction


class Actions:
    def __init__(self):
        pass


class Handler:
    def __init__(self, event):
        self.actions = {}

        func_list = [o for o in getmembers(Actions) if isfunction(o[1])]

        for func in func_list:
            self.actions[func[0]] = func[1]

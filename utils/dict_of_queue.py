from queue import Queue

# This class is used to store a dictionary of queues
class DictOfQueue:
    def __init__(self):
        self._dict = {}

    def add_value(self, key, value):
        if key not in self._dict:
            self._dict[key] = Queue()
        
        self._dict[key].put(value)

    def get_and_remove_first_value(self, key):
        if key in self._dict and self._dict[key]:
            inner_values = self._dict[key].get()
            return inner_values
        else:
            return None
        
    def get_first_value(self, key):
        if key in self._dict:
            return self._dict[key][0]
        else:
            return None
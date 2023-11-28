
# Simple interface for model wrappers
# Integration with other models should be simply done by implementing this interface
class Wrapper:
    def __init__(self, model):
        self.model = model

    def get_probability(self, sequence, symbols):
        return NotImplementedError
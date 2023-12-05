
# Simple interface for model wrappers
# Integration with other models should be simply done by implementing this interface
class Wrapper:
    def __init__(self, model):
        self.model = model

    # Receives a sequence of symbols as an string and a list of symbols to predict
    # Returns a dictionary with the probabilities for each symbol
    def get_probability(self, sequence:str, symbols:list):
        return NotImplementedError
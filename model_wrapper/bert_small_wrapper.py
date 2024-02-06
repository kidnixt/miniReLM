from model_wrapper.model_wrapper import Wrapper
import torch

class BertSmallWrapper(Wrapper):
    def __init__(self, model, tokenizer, device):
        super().__init__(model, tokenizer)
        self.model = model
        self.tokenizer = tokenizer
        self.device = device

    def get_probability(self, sequence: str, symbols: list):
        input = self.tokenizer(sequence, return_tensors="pt").to(self.device)

    

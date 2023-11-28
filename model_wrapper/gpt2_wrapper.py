from model_wrapper.wrapper import Wrapper
import torch


class GPT2Wrapper(Wrapper):
    def __init__(self, model, tokenizer, device):
        super().__init__(model)
        self.tokenizer = tokenizer
        self.device = device

    def tokenize(self, sequence):
        return torch.tensor([self.tokenizer.bos_token_id,] + self.tokenizer.encode(sequence)).reshape(1, -1).to(self.device)

    def get_probability(self, sequence, symbols, top_k=None):
        
        input_ids = self.tokenize(sequence)
        
        with torch.no_grad():
            output = self.model(input_ids)
            logits = output[0]
            probs = logits.softmax(-1)
            _axis = len(probs.shape) - 1
            top_k_val = torch.topk(probs, axis=_axis, k=top_k)
            probs[:] = 0.
            probs = probs.scatter(_axis,
                            top_k_val.indices,
                            top_k_val.values)
            probs /= torch.sum(probs)

        self.get_words_probabilities(probs, symbols)

    def get_words_probabilities(self, probs, symbols):
        for symbol in symbols:
            word = self.tokenizer.encode(symbol)
            word_id = torch.tensor(word).reshape(1, -1).to(self.device)
            word_prob = torch.gather(probs, 1, word_id).item()
            print(f"{symbol}: {word_prob}")

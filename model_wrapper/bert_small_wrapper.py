from model_wrapper.model_wrapper import Wrapper
import torch

class BertSmallWrapper(Wrapper):
    def __init__(self, model, tokenizer, device):
        super().__init__(model)
        self.tokenizer = tokenizer
        self.device = device

    def tokenize(self, sequence: str):
        return self.tokenizer(sequence, return_tensors="pt").to(self.device)

    def get_probability(self, sequence: str, symbols: list):
        tokens = self.tokenize(sequence)
        print((tokens.input_ids))
        with torch.no_grad():
            output = self.model(tokens.input_ids)
            logits = output.logits
            probs = torch.softmax(logits, dim=-1)

        word_probabilities = {}
        for word in symbols:
            print(word)
            print(type(word))
            #cast the word to string
            word = str(word)
            word_tokens = self.tokenize(word)
            print(word_tokens)
            print(word_tokens.input_ids)
            word_probs = probs[:, word_tokens.input_ids[0]]
            total_word_probs = sum(word_probs)
            total_word_probs /= len(word_probs)
            word_probabilities[word] = total_word_probs.item()

        total = sum(word_probabilities.values())
        for word in word_probabilities:
            word_probabilities[word] /= total

        return word_probabilities
    



    
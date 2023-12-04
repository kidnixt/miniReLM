from model_wrapper.model_wrapper import Wrapper
import torch


class GPT2Wrapper(Wrapper):
    def __init__(self, model, tokenizer, device):
        super().__init__(model)
        self.tokenizer = tokenizer
        self.device = device

    def tokenize(self, sequence):
        return torch.tensor([self.tokenizer.bos_token_id,] + self.tokenizer.encode(sequence)).reshape(1, -1).to(self.device)

    def tokenize_empty(self):
        return torch.tensor([self.tokenizer.bos_token_id,]).reshape(1, -1).to(self.device)

    def get_probability(self, sequence, symbols, top_k=None):
        if sequence == "":
            input_ids = self.tokenize_empty()
        else:
            input_ids = self.tokenize(sequence)
        
        with torch.no_grad():
            output = self.model(input_ids)
            # logits = output[0]
            # probs = logits.softmax(-1)
            logits = output.logits[:, -1, :]
            probs = torch.softmax(logits, dim=-1)
            if top_k is not None:
                _axis = len(probs.shape) - 1
                top_k_val = torch.topk(probs, axis=_axis, k=top_k)
                probs[:] = 0.
                probs = probs.scatter(_axis,
                                top_k_val.indices,
                                top_k_val.values)
                probs /= torch.sum(probs)

        return self.get_words_probabilities(probs, symbols)

    # TODO: We should make sure that we are calculating the probabilities for the correct words
    # Since the tokenizer splits words in different ways, we should check that the probabilities
    # make sense
    def get_words_probabilities(self, probs, symbols):
        word_probabilities = {}
        for word in symbols:
            word_tokens = self.tokenizer.tokenize(word.value)
            # Convert each tokenization to input IDs
            input_ids_list = [self.tokenizer.encode(token) for token in word_tokens]
            # Extract probabilities for the specified words from the distribution of the next token
            word_probs = [probs[:, token_id] for token_id in input_ids_list]
            # Sum the probabilities for all tokenizations of the word
            total_word_probs = torch.stack(word_probs, dim=-1).sum(dim=-1, keepdim=True)
            # total_word_probs /= total_word_probs.sum(dim=-1, keepdim=True)
            word_probabilities[word.value] = total_word_probs[0, -1, 0].item()
            
        # Normalize the probabilities
        total = sum(word_probabilities.values())
        for word in word_probabilities:
            word_probabilities[word] /= total

        
        return word_probabilities

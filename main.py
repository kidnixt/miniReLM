import torch
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer

def main():
    torch.manual_seed(42)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_id = "gpt2"  # Change this to "gpt2" if you get memory issues

    tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(model_id,
                                                return_dict_in_generate=True,
                                                pad_token_id=tokenizer.eos_token_id).to(device)

    prompt = "The man was trained in"
    input_ids = torch.tensor([tokenizer.bos_token_id,] + tokenizer.encode(prompt)).reshape(1, -1).to(device)
    # Generate responses from the model (in tokens)
    tokens = model.generate(input_ids,
                            max_new_tokens=20,
                            num_return_sequences=10,
                            do_sample=True).sequences
    # Print the strings representing the responses
    for t in tokens:
        # print(tokenizer.decode(t[1:]))
        pass

    # Get the probability of the word 'medicine' at the end of the generated text
    
    index = tokenizer.encode("man")

    with torch.no_grad():
        output = model(input_ids)
        logits = output[0]
        probs = logits.softmax(-1)
        # print(probs.shape)

    prob = probs[0, -1, index[0]].item()
    print(f"Probability of 'medicine' is {prob:.4f}")
    prob = probs[0, -1, index[1]].item()
    print(f"Probability of 'medicine' is {prob:.4f}")
    prob = probs[0, -1, index[2]].item()
    print(f"Probability of 'medicine' is {prob:.4f}")

if __name__ == "__main__":
    main()
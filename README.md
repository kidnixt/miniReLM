# miniReLM
ReLM chiquito

Implementation of the MiniReLM model we proposed in the paper "MiniReLM: A Comprehensive Validation Approach Inspired by ReLM"

The notebooks in this project serve as a guide to reproduce the experiments in the paper.

## Quick guide of use

- You need to install ***Pythautomata*** for this library to work
- This library can be use with any Language Model, it is only **required to implement the model_wrapper interface. There is one already created for GPT2**
- The Regex to Automaton parser is not implemented yet, so you need to create the automaton yourself. There are examples of use in automata_examples folder, and you use the Pythautomata library to create the automaton
  

## Automata Examples


In the ***automata_examples*** folder you can find examples of how to create automata using the *pythautomata* library. The provided examples uses the library to define a Deterministic Finite Automaton (DFA), that represents a specific pattern in a language based on a regular expression.

  
1. Import the necessary classes from the *pythautomata* library

2. Define the alphabet that the automaton will accept. In the ***"man_woman_dfa.py",*** the alphabet consists of the words `"The", "man", "woman", "studied", "medicine", "science", "engineering", "maths", "art", and "music".`

3. Define the transitions and states of the automaton. A DFA is being constructed to represent the following regex pattern: `"The (man|woman) studied (medicine|science|engineering|maths|art|music)"`. Each state represents a step in the string that the automaton is accepting.

4. The automaton is created using the "***DeterministicFiniteAutomaton***" class from the *pythautomata* library. The states, transitions, alphabet and a comparator to determine the equivalence of two DFAs, are passed as parameters to the constructor.

## Model Wrapper 

The wrapper is used to interact with the language model and to obtain the probabilities of the words in the language model.
The wrapper is an interface that needs to be implemented by the user. There is already an implementation for GPT2 in the ***model_wrappers*** folder.

- The main method of the wrapper is ***get_probabilities***, which receives a list of words and returns a list of probabilities for each word.
  - sequence: A sequence of symbols provided by the user, as a string.
  - symbols: A list of symbols that the user wants to obtain the probabilities for.


The method returns a dictionary with the probabilities for each symbol. However, the actual implementation of how the probabilities are obtained is left to the specific model wrapper that inherits from this interface.

### GPT2 Wrapper

- GPT2Wrapper is a class that inherits from the previously defined Wrapper class. It represents a wrapper for a GPT-2 model. The class provides methods to tokenize input sequences, compute probabilities for the next token, and compute probabilities for specified words based on the distribution of the next token.
- The constructor (__init__) initializes an instance of the class, taking the GPT-2 model (model), tokenizer (tokenizer), and device (device) as parameters. 
- The *tokenize* method converts a sequence into tokenized input IDs using the GPT-2 tokenizer and returns a tensor on the specified device. 
- The *tokenize_empty* method tokenizes an empty sequence. 
- The **get_probability** method takes a sequence, symbols to predict, and an optional top_k parameter. It computes the probabilities for the next symbols in the sequence using the GPT-2 model. The **top_k** parameter specifies the number of top tokens to consider for the next token prediction. 
- The ***get_words_probabilities*** method computes probabilities for specified words based on the distribution of the next token. It normalizes probabilities by the number of tokens for each word. 


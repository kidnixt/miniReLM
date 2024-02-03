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

-------------
### GPT2 Wrapper

The `GPT2Wrapper` class serves as a model wrapper for interacting with a GPT-2 language model. It implements the `Wrapper` interface, allowing seamless integration with other language models through a consistent interface. The wrapper is designed to provide probabilities for predicting the next symbols in a given sequence.

#### Dependencies

The code relies on the following external libraries:

- `pythautomata`: A Python library for working with automata.
- `model_wrapper`: A custom module providing a generic interface (`Wrapper`) for interacting with language models.

#### Methods

- #### `__init__(self, model, tokenizer, device)`: 
  - Initializes an instance of the GPT2Wrapper class with a GPT-2 model (`model`), tokenizer (`tokenizer`), and device (`device`).

- #### `tokenize(self, sequence) -> torch.Tensor`:
  - Tokenizes a given sequence using the GPT-2 tokenizer.

- #### `tokenize_empty(self) -> torch.Tensor`:
  - Tokenizes an empty sequence using the GPT-2 tokenizer.

- #### `get_probability(self, sequence, symbols, top_k=None) -> dict`:
  - Computes probabilities for predicting the next symbols in a given sequence using the GPT-2 model.
  - Supports an optional `top_k` parameter to consider only the top-k likely symbols.

- #### `get_words_probabilities(self, probs, symbols) -> dict`:
  - Computes probabilities for specified words based on the distribution of the next token.
  - Normalizes probabilities by considering the number of tokens for each word.

## LLM Automaton 

### LLMAutomatonBuilder

The `LLMAutomatonBuilder` class is designed to construct a Probabilistic Deterministic Finite Automaton (PDFA) from a given Regex Automaton. The process involves traversing the Regex Automaton and querying a Language Model (LLM) represented by the `Wrapper` class to obtain probabilities for symbol transitions. The resulting PDFA represents the language modeled by the original Regex Automaton.

#### Dependencies

The code relies on the following external libraries:

- `pythautomata`: A Python library for working with automata.
- `model_wrapper`: A custom module providing a generic interface (`Wrapper`) for interacting with language models.
- `utils`: A module containing a custom data structure (`DictOfQueue`) and miscellaneous utility functions.


### Methods

- #### `construct_llm_automaton(regex_automaton: DeterministicFiniteAutomaton, llm: Wrapper) -> ProbabilisticDeterministicFiniteAutomaton`:
  - Constructs a Probabilistic Deterministic Finite Automaton (PDFA) based on a given Regex Automaton and a Language Model (LLM).
  - Utilizes a Breadth-First Search (BFS) approach to traverse the Regex Automaton.
  - Queries the LLM for symbol probabilities and constructs the PDFA accordingly.

### Helper Functions

#### `search_state_by_sequence(sequence: Sequence, initial_state: WeightedState) -> WeightedState`:

- Searches for a state in the PDFA based on a given sequence.

#### `process_state_transitions(sequenceForStates: dict[State, Sequence], state: State, llm: Wrapper, pdfa_initial_state: WeightedState, pdfa_states: set[WeightedState], statesToVisit: list[State], visitedStates: set[State], alphabet: set[SymbolStr]) -> set[WeightedState]`:

- Processes transitions for a state in the Regex Automaton.
- Queries the LLM for probabilities and updates the PDFA states accordingly.

#### `create_pdfa_state(symbols: set[SymbolStr], initial_weight: float = 0, final_weight: float = 0) -> WeightedState`:

- Creates a new WeightedState for the PDFA with initial and final weights.
- Ensures uniqueness by generating a random name.

#### `upsert_transition(state: WeightedState, symbol: SymbolStr, new_state: WeightedState, probability: float)`:

- Inserts or updates a transition in the PDFA for a given symbol and state.

#### `sequence_to_string(sequence: Sequence) -> str`:

- Converts a sequence of symbols to a string for querying the LLM.

-------------


### LLMAutomatonSampler

The `LLMAutomatonSampler` class serves as a sampler for a Probabilistic Deterministic Finite Automaton (PDFA) represented by the `ProbabilisticDeterministicFiniteAutomaton` class. It generates random samples from the PDFA, considering the probabilities associated with transitions.

#### Dependencies

The code relies on the following external libraries:

- `pythautomata`: A Python library for working with automata.

#### Methods

- #### `__init__(self, automaton: ProbabilisticDeterministicFiniteAutomaton)`: 
  - Initializes an instance of the `LLMAutomatonSampler` class with a PDFA (`automaton`).

- #### `sample(self, n_samples: int) -> list`:
  - Generates a specified number of samples from the PDFA.
  - Returns a list of samples, where each sample is a sequence of symbols.

#### Internal Methods

- #### `_sample(self) -> list`:
  - Generates a single sample from the PDFA.
  - Returns a list representing the sample.

- #### `_sample_from_state(self, state: State) -> Tuple[State, Symbol]`:
  - Generates a sample from a specific state in the PDFA.
  - Returns the sampled state and the associated symbol.
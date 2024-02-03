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

## LLM Automaton

# miniReLM
ReLM chiquito

Implementation of the MiniReLM model we proposed in the paper "MiniReLM: A Comprehensive Validation Approach Inspired by ReLM"

The notebooks in this project serve as a guide to reproduce the experiments in the paper.

## Quick guide of use

- You need to install Pythautomata for this library to work
- This library can be use with any Language Model, it is only required to implement the model_wrapper interface. There is one already created for GPT2
- The Regex to Automaton parser is not implemented yet, so you need to create the automaton yourself. There are examples of use in automata_examples folder, and you use the Pythautomata library to create the automaton
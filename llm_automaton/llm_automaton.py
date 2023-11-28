# In this file we will traverse the regex automaton and 
# generate a PDFA?
from pythautomata.automata.deterministic_finite_automaton import DeterministicFiniteAutomaton
from pythautomata.base_types.state import State
from pythautomata.base_types.symbol import Symbol
from pythautomata.base_types.sequence import Sequence


def aaaaa(sequenceForStates: dict[State, Sequence], state: State, llm):
    # Here we need all the symbols in the transitions
    # If we assume the DFA is complete, we could simply use th alphabet here
    sequence = sequenceForStates[state]
    transitions = state.transitions
    if len(transitions) == 0:
        # We are in a final state
        return
    if len(transitions) == 1:
         # We don't need to ask the llm the probability
         # We can simply assume it is 1
         # add the transition to the llm automaton
         return
    
    symbols = [transition.symbol for transition in transitions]
    probs = llm.get_probability(sequence, symbols)
        # add the transition to the llm automaton
        # add the transition to the sequence
        # add the next state to the states to visit

def construct_llm_automaton(regex_automaton: DeterministicFiniteAutomaton, llm):
    # Traverse the regex_automaton in a DFS manner
    # for each node, take the transitions and ask a query to the llm
    # create a new node in the llm automaton and add the transitions
    # with the probabilities returned by the llm

     # initialPairs is an arbitrary pair of states
        initialState = regex_automaton.initial_state
        statesToVisit = [initialState]
        sequenceForStates = {initialState: Sequence()}
        visitedState: set[State] = set()

        while statesToVisit:
            state = statesToVisit[0]
            aaaaa(sequenceForStates, state, llm)
            statesToVisit.remove(state)
            visitedState.add(state)
        return None


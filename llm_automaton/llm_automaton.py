from pythautomata.automata.deterministic_finite_automaton import DeterministicFiniteAutomaton
from pythautomata.automata.wheighted_automaton_definition.probabilistic_deterministic_finite_automaton import \
    ProbabilisticDeterministicFiniteAutomaton
from pythautomata.base_types.state import State
from pythautomata.base_types.symbol import SymbolStr
from pythautomata.base_types.sequence import Sequence
from pythautomata.automata.wheighted_automaton_definition.weighted_state import WeightedState
from pythautomata.model_comparators.wfa_tolerance_comparison_strategy import WFAToleranceComparator
from model_wrapper.model_wrapper import Wrapper
import string
import random

# Traverses the regex automaton and generate a PDFA
class LLMAutomatonBuilder:

    def construct_llm_automaton(self, regex_automaton: DeterministicFiniteAutomaton, llm:Wrapper):
        # Traverse the regex_automaton in a DFS manner
        # for each node, take the transitions and ask a query to the llm
        # create a new node in the llm automaton and add the transitions
        # with the probabilities returned by the llm

        pdfa_states = set()
        pdfa_initial_state = WeightedState(name = regex_automaton.initial_state.name, initial_weight=1, final_weight=0)
        pdfa_states.add(pdfa_initial_state)

        # initialPairs is an arbitrary pair of states
        initialState = regex_automaton.initial_state
        statesToVisit = [initialState]
        sequenceForStates = {initialState: Sequence()}
        visitedStates: set[State] = set()
        while statesToVisit:
            state = statesToVisit[0]
            process_state_transitions(sequenceForStates, state, llm, pdfa_initial_state, pdfa_states, statesToVisit, visitedStates, regex_automaton.alphabet.symbols)
            statesToVisit.remove(state)
            visitedStates.add(state)

        comparator = WFAToleranceComparator()
        return ProbabilisticDeterministicFiniteAutomaton(regex_automaton.alphabet, pdfa_states, SymbolStr("$"), comparator, "llm_automaton")

def search_state_by_sequence(sequence: Sequence, initial_state: WeightedState):
    actual_state = initial_state
    for symbol in sequence:
        for symbol, states in actual_state.transitions_list.items():
            if symbol == symbol:
                # transtitions_list is a dict, of symbol -> list of tuple (state, probability)
                actual_state = states[0][0] # We assume the automaton is deterministic
        
    return actual_state


def process_state_transitions(sequenceForStates: dict[State, Sequence], state: State, llm: Wrapper, pdfa_initial_state: WeightedState, 
                              pdfa_states: set[WeightedState], statesToVisit: list[State], visitedStates: set[State], alphabet: set[SymbolStr]):

    sequence = sequenceForStates[state]
    actual_pdfa_state = search_state_by_sequence(sequence, pdfa_initial_state)

    # if state.is_final:
    #     actual_pdfa_state.final_weight = 0.3

    transitions = state.transitions
    symbols = []
    for symbol, _ in transitions.items():
        symbols.append(symbol)

    # Here we need all the symbols in the transitions
    # If we assume the DFA is complete, we could simply use th alphabet here
    sequence = sequenceForStates[state]
    
    if len(transitions) == 0:
        # We are in a final state
        actual_pdfa_state.final_weight = 1
        return pdfa_states
    if len(transitions) == 1:
        # We don't need to ask the llm the probability, we can simply assume it is 1
        new_state = create_pdfa_state(alphabet, state)
        pdfa_states.add(new_state)
        transition_symbol = list(transitions.keys())[0]
        upsert_transition(actual_pdfa_state, transition_symbol, new_state, 1.0)
        next_state = min(state.next_states_for(transition_symbol))
        if next_state not in visitedStates:
            statesToVisit.append(next_state)
            # TODO: here should be a way to get all the sequences that lead to this state
            # For example: "The man" and "The woman" leads to the same state
            # And we want to keep both sequences 
            sequenceForStates[next_state] = sequenceForStates[state] + transition_symbol
        return pdfa_states
    
    string = sequence_to_string(sequence)

    probs = llm.get_probability(string, symbols)
    for symbol in symbols:
        new_state = create_pdfa_state(alphabet, state)
        pdfa_states.add(new_state)
        upsert_transition(actual_pdfa_state, symbol, new_state, probs[str(symbol.value)])
        # actual_pdfa_state.add_transition(symbol, new_state, probs[str(symbol.value)])
        next_state = min(state.next_states_for(symbol))
        if next_state not in visitedStates:
            statesToVisit.append(next_state)
            sequenceForStates[next_state] = sequenceForStates[state] + symbol


    return pdfa_states
    

def create_pdfa_state(symbols: set[SymbolStr], state: State):
    alphanumeric_chars = string.ascii_letters + string.digits
    
    new_state = WeightedState(name=random.choice(alphanumeric_chars), initial_weight=0, final_weight=0)
    # We create a transition for each symbol, to make sure the automaton is complete or else the init function will fail
    for symbol in symbols :
        new_state.add_transition(symbol, new_state, 0.0)

    return new_state

# Since we created the state with placeholder transitions and the pythautomata library allows to have multiple transitions for the same symbol,
# which is not what we want. We need to clear the transitions for that symbol and add the new one 
def upsert_transition(state: WeightedState, symbol: SymbolStr, new_state: WeightedState, probability: float):
    if symbol not in state.transitions_set:
        state.add_transition(symbol, new_state, probability)
    else:
        # Clear transitions for that symbol
        state.transitions_set[symbol] = set()
        state.transitions_list[symbol] = list()
        state.add_transition(symbol, new_state, probability)
    
    

def sequence_to_string(sequence: Sequence):
    string = ""
    for symbol in sequence:
        string += (f" {symbol.value}")
    return string


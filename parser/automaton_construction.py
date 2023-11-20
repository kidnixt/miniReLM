from pythautomata.automata.non_deterministic_finite_automaton import NondeterministicFiniteAutomaton
from pythautomata.base_types.state import State
from pythautomata.base_types.alphabet import Alphabet
from pythautomata.base_types.symbol import Symbol, SymbolStr
from pythautomata.model_comparators.dfa_comparison_strategy import DFAComparisonStrategy
from pythautomata.model_exporters.standard_exporters.dfa_standard_dot_exporting_strategy import DfaStandardDotExportingStrategy
from pythautomata.model_exporters.dot_exporters.dfa_dot_exporting_strategy import DfaDotExportingStrategy
from pythautomata.utilities.automata_converter import AutomataConverter
from pythautomata.utilities.dfa_minimizer import DFAMinimizer
from fiumba2 import tokenize_regex, shunting_yard_regex

def get_final(nfa):
    # Assume that thompson construction always returns an NFA with a single final state
    for state in nfa.states:
        if state.is_final:
            return state
        
def get_initial(nfa):
    # Assume that thompson construction always returns an NFA with a single initial state
    for state in nfa.initial_states:
            return state

# Thomposon's construction
def automaton_construction(postfix):
    # Stack for NFAs
    nfa_stack = [NondeterministicFiniteAutomaton]

    counter = 0

    for c in postfix:
        print("Now processing", c, "\n")
        if c == '.':
            # pop 2 NFA's off the stack
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            nfa2_initial = get_initial(nfa2)
            get_final(nfa1).add_transition(SymbolStr('e'), nfa2_initial)
            get_final(nfa1).is_final = False

            newAlphabet = nfa1.alphabet.symbols | nfa2.alphabet.symbols | frozenset([SymbolStr('e')])


            states = nfa1.states.union(nfa2.states)
            initial = nfa1.initial_states
            nfa = NondeterministicFiniteAutomaton(alphabet=Alphabet(newAlphabet), initial_states= initial, 
                                                  states = states, comparator=DFAComparisonStrategy,
                                                  exportingStrategies=[DfaDotExportingStrategy()])
            # push new NFA to the stack
            nfa_stack.append(nfa)

        elif c == '|':
           # pop 2 NFAs off the stack.
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            # create a new initial state, connect it to 
            # initial states of the two NFAs popped from the stack
            initial = State(f"q{counter}", False)
            counter += 1
            nfa1_initial = get_initial(nfa1)
            initial.add_transition(SymbolStr('e'), nfa1_initial)
            nfa2_initial = get_initial(nfa2)
            initial.add_transition(SymbolStr('e'), nfa2_initial)
            # create new accept state, connecting the accept states 
            # of the 2 NFAs popped from the stack, to the new state
            final = State(f"q{counter}", True)
            counter += 1
            nfa1_final = get_final(nfa1)
            nfa1_final.is_final = False
            nfa1_final.add_transition(SymbolStr('e'), final)

            nfa2_final = get_final(nfa2)
            nfa2_final.is_final = False
            nfa2_final.add_transition(SymbolStr('e'), final)

            newAlphabet = nfa1.alphabet.symbols | nfa2.alphabet.symbols | frozenset([SymbolStr('e')])
            states = nfa1.states.union(nfa2.states)
            states.add(initial)
            states.add(final)

            # push NFA to stack
            nfa = NondeterministicFiniteAutomaton(alphabet=Alphabet(newAlphabet), initial_states= frozenset({initial}), 
                                                  states = states, comparator=DFAComparisonStrategy,
                                                  exportingStrategies=[DfaDotExportingStrategy()])
            nfa_stack.append(nfa)
        elif c == '*':
            pass
        else :
            initial = State(f"q{counter}", False)
            counter += 1
            final = State(f"q{counter}", True)
            counter += 1
            symbol = SymbolStr(c)
            initial.add_transition(symbol, final)
            alphabet = Alphabet(frozenset([symbol]))
            nfa = NondeterministicFiniteAutomaton(
                alphabet= alphabet, initial_states = frozenset({initial}), 
                states = set({initial, final}), comparator = DFAComparisonStrategy, exportingStrategies=[DfaDotExportingStrategy()])
            nfa_stack.append(nfa)

    return nfa_stack.pop()

# Usage example
regex = "The (man|woman) is"
tokenized = tokenize_regex(regex)
postfix_result = shunting_yard_regex(tokenized)
print("postfix_result:", postfix_result)
nfa = automaton_construction(postfix_result)
converter = AutomataConverter()
dfa = converter.convert_nfa_to_dfa(nfa)
dfa._exporting_strategies = [DfaStandardDotExportingStrategy()]
minimizer = DFAMinimizer(dfa)
minimized_dfa = minimizer.minimize()
minimized_dfa._exporting_strategies = [DfaStandardDotExportingStrategy()]
minimized_dfa.export()

def epsilon_closure_removal(dfa):
    #     Compute Epsilon Closure for States:
    #     For each state in the DFA, compute its epsilon closure. The epsilon closure of a state is the set of states reachable from it using epsilon transitions.
    for state in dfa.states:
        epsilon_closure = set()
        for transition, state in state.transitions:
            if transition.symbol == SymbolStr('e'):
                epsilon_closure.add(state)

    # Modify Transition Function:
    #     Modify the transition function to eliminate epsilon transitions. For each state, combine the transitions reachable through epsilon closure into a single transition.

    # Remove Epsilon-Labeled States:
    #     Remove the epsilon-labeled states from the set of states.

    # Update Accepting States:
    #     Update the set of accepting states if necessary.

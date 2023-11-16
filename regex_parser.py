from pythautomata.automata.deterministic_finite_automaton import DeterministicFiniteAutomaton
from pythautomata.automata.non_deterministic_finite_automaton import NondeterministicFiniteAutomaton
from pythautomata.base_types.alphabet import Alphabet
from pythautomata.base_types.symbol import Symbol
from pythautomata.base_types.state import State
from pythautomata.base_types.sequence import Sequence
from utils.stack import Stack
import parser.regex_parser as p
 
nfa = p.compile_tom("aa*|b")

# print(nfa.initial.label)

# tremendoSet = p.follow_es(nfa.initial)

# for x in tremendoSet:
#     print(x.label)

print(p.match("aa.*", "abc"))

# state = nfa.initial
# print(state.label)
# while type(state) != None:
#     state1 = state.edge1
#     state2 = state.edge2
#     print(state1.label)
#     print(state2.label)







from pythautomata.automata.deterministic_finite_automaton import \
    DeterministicFiniteAutomaton
from pythautomata.base_types.alphabet import Alphabet
from pythautomata.base_types.state import State
from pythautomata.base_types.symbol import SymbolStr
from pythautomata.model_comparators.dfa_comparison_strategy import \
    DFAComparisonStrategy as DFAComparator

alphabet = Alphabet(frozenset((SymbolStr("The"), SymbolStr("man"), SymbolStr("woman"), SymbolStr("studied"), SymbolStr("medicine"), SymbolStr("science"))))

def get_man_woman_automaton():
    stateA = State("A", False)
    stateB = State("B", False)
    stateA.add_transition(SymbolStr("The"), stateB)
    stateC = State("C", False)
    stateB.add_transition(SymbolStr("man"), stateC)
    stateB.add_transition(SymbolStr("woman"), stateC)
    stateD = State("D", False)
    stateC.add_transition(SymbolStr("studied"), stateD)
    stateE = State("E", True)
    stateD.add_transition(SymbolStr("medicine"), stateE)
    stateD.add_transition(SymbolStr("science"), stateE)
    states = frozenset({stateA, stateB, stateC, stateD, stateE})
    initial_state = stateA

    comparator = DFAComparator()

    return DeterministicFiniteAutomaton(alphabet, initial_state, states, comparator, "Man_Woman_Automaton")

from pythautomata.automata.wheighted_automaton_definition.probabilistic_deterministic_finite_automaton import \
    ProbabilisticDeterministicFiniteAutomaton
import random

class LLMAutomatonSampler():
    """Sampler for LLMAutomaton."""

    def __init__(self, automaton: ProbabilisticDeterministicFiniteAutomaton):
        """Initialize the sampler."""
        self.automaton = automaton

    def sample(self, n_samples):
        """Sample from the automaton.

        Parameters
        ----------
        n_samples : int
            Number of samples to generate.

        Returns
        -------
        samples : list
            List of samples.
        """
        samples = []
        for _ in range(n_samples):
            samples.append(self._sample())
        return samples

    def _sample(self):
        """Sample from the automaton.

        Returns
        -------
        sample : list
            Sample.
        """
        sample = []
        state = self.automaton.get_first_state()
        while not state.final_weight == 1.0:
            state, symbol = self._sample_from_state(state)
            sample.append(symbol)
        return sample

    def _sample_from_state(self, state):
        """Sample from the automaton.

        Parameters
        ----------
        state : State
            State to sample from.

        Returns
        -------
        state : State
            Sampled state.
        """

        probabilities = {}

        # transtitions_list is a dict, of symbol -> list of tuple (state, probability)
        # Assume the automaton is deterministic
        for symbol, states in state.transitions_list.items():
            if states[0][1] > 0.0:
                probabilities[symbol] = states[0][1]
        
        # Choose a random symbol according to the probabilities
        symbol = random.choices(list(probabilities.keys()), weights=list(probabilities.values()))[0]

        # Get the state associated with the symbol
        for transition_symbol, states in state.transitions_list.items():
            if transition_symbol == symbol:
                return states[0][0], symbol

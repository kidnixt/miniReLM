# Thompson's Construction
# represents a state with two arrows, labelled by label
# use 'None' for a label representing  'Ɛ' arrows
class state:
    label = None
    edge1 = None
    edge2 = None


# an NFA is represented by its initial and accepts states
class nfa:
    initial = None
    accept = None

    # mandatory to have 'self' args in constructor
    def __init__(self, initial, accept):
        self.initial = initial
        self.accept = accept


# Algorithm
# function has a stack of NFAs
# pofix allows to loop one character at a time
# until the regular expression is complete
def compile_tom(pofix):
    nfa_stack = []

    for c in pofix:
        if c == '.':
            # stack works as last in first out
            # method to go to stack
            # pop 2 NFAs off the stack.
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            # merges them together
            # connect 1st NFAs accept state to the 2nd's initial
            nfa1.accept.edge1 = nfa2.initial

            # push NFA to stack
            # one way to do it ¬ nfa_stack.append(nfa(initial, accept))
            # second way 'easier way'
            new_nfa = nfa(nfa1.initial, nfa2.accept)
            # push new_nfa
            nfa_stack.append(new_nfa)

        elif c == '|':
            # pop 2 NFAs off the stack.
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            # create a new initial state, connect it to 
            # initial states of the two NFAs popped from the stack
            initial = state()
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            # create new accept state, connecting the accept states 
            # of the 2 NFAs popped from the stack, to the new state
            accept = state()
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept

            # push NFA to stack
            # one way to do it ¬ nfa_stack.append(nfa(initial, accept))
            # second way 'easier way'
            new_nfa = nfa(initial, accept)
            # push new_nfa
            nfa_stack.append(new_nfa)

        elif c == '*':
            # pop a single NFA from the stack
            nfa1 = nfa_stack.pop()
            # create a new initial and accept states
            initial = state()
            accept = state()
            # join the new initial state to nfa1's initial state and the new accept state.
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            # join the old accept state to the new accept state and nfa1's initial state.
            nfa1.accept.edge1 = nfa.initial
            nfa1.accept.edge2 = accept

            # push new NFA to the stack
            # one way to do it ¬ nfa_stack.append(nfa(initial, accept))
            # second way 'easier way'
            new_nfa = nfa(initial, accept)
            # push new_nfa
            nfa_stack.append(new_nfa)

        elif c == '+':
            # pop nfa from stack
            nfa1 = nfa_stack.pop()
            # create a new initial and accept states
            initial = state()
            accept = state()
            # join the new initial stse to nfa1's initial state and the new accept state.
            initial.edge1 = nfa1.initial
            # join the old accept state to the new accept state and nfa1's initial state.
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            # push new NFA to the stack
            new_nfa = nfa(initial, accept)
            # pushes new_nfa
            nfa_stack.append(new_nfa)

        elif c == '?':
            # pop nfa from stack
            nfa1 = nfa_stack.pop()
            # create a new initial and accept states
            initial = state()
            accept = state()
            # join the new initial stse to nfa1's initial state and the new accept state.
            initial.edge1 = nfa1.initial
            initial.edge2 = accept
            # join the old accept state to the new accept state and nfa1's initial state.
            nfa1.accept.edge1 = nfa1.initial
            nfa1.accept.edge2 = accept
            # push new NFA to the stack
            new_nfa = nfa(initial, accept)
            # pushes new_nfa
            nfa_stack.append(new_nfa)

        else:
            # create new initial and accept states
            # creates new nfa
            accept = state()
            # creates new nfa
            initial = state()
            # string character
            # joins the initial states to the accept state
            # using an arrow labelled c.
            initial.label = c
            initial.edge1 = accept
            # going to create a new instance of the NFA class. 
            # set its initial state to the 
            # initial state

            # push new NFA to the stack # ¬ returns an instance of the nfa class ¬
            # one way to do it ¬ nfa_stack.append(nfa(initial, accept))
            # second way 'easier way'
            new_nfa = nfa(initial, accept)
            # push new_nfa
            nfa_stack.append(new_nfa)

    # nfa_stack  should only have a single nfa on it at the point.
    return nfa_stack.pop()


#
# Return the set of states that can be reached from state following e arrows
def follow_es(following_state):
    # create a new set, with state as its only member
    states = set()
    states.add(following_state)

    # check if state has arrows labeled e from it
    if following_state.label is None:
        # Check if edge1 is a state
        if following_state.edge1 is not None:
            # if there's an edge1, follow it
            states |= follow_es(following_state.edge1)
        # check if edge2 is a state
        if following_state.edge2 is not None:
            # if there's an edge2, follow it
            states |= follow_es(following_state.edge2)

    # return the set of states
    return states


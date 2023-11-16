def regex_to_postfix(regex):
    precedence = {'*': 3, '+': 3, '?': 3, '.': 2, '|': 1, '^': 0, '(': 0}  # Operator precedence
    output = []  # Output list (postfix notation)
    operator_stack = []  # Operator stack

    i = 0
    while i < len(regex):
        char = regex[i]

        if char.isalnum():
            output.append(char)  # Add operands directly to the output
            # Add '.' operator explicitly if the next character is alphanumeric
            if i < len(regex) - 1 and regex[i + 1].isalnum():
                output.append('.')
        elif char == '(':
            operator_stack.append(char)
        elif char == ')':
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()  # Pop '(' from the stack
        else:
            # Operator processing
            if i < len(regex) - 1 and regex[i + 1] == '*':
                operator_stack.append('(')
                output.append(char)
                i += 1  # Skip the '*'
                while i < len(regex) and regex[i] == '*':
                    output.append('*')
                    i += 1
                operator_stack.append(')')
                continue  # Continue with the next iteration

            while operator_stack and precedence.get(char, 0) <= precedence.get(operator_stack[-1], 0):
                output.append(operator_stack.pop())
            operator_stack.append(char)

        i += 1

    while operator_stack:
        output.append(operator_stack.pop())

    return ''.join(output)

# Usage example
regex = "e|a*.b"
postfix = regex_to_postfix(regex)
print(f"Regular Expression: {regex}")
print(f"Postfix Notation: {postfix}")

def regex_to_postfix(regex):
    precedence = {'*': 3, '+': 3, '?': 3, '.': 2, '|': 1, '^': 0, '(': 0}  # Operator precedence
    output = []  # Output list (postfix notation)
    operator_stack = []  # Operator stack

    regex = tokenize_regex(regex)

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


import re

def tokenize_regex(regex_pattern):
    # Add spaces around the special characters to simplify splitting
    regex_pattern = re.sub(r'([\(\)\|\*])', r' \1 ', regex_pattern)
    
    # Split the regex into tokens
    tokens = re.findall(r'\S+|\s+', regex_pattern)
    
    # Remove spaces from tokens
    tokens = [item for item in tokens if not item.isspace()]

    # Add operator '.' explicitly if the next token is a word character or '('
    i = 0
    while i < len(tokens) - 1:
        if tokens[i] == ')' or tokens[i].isalnum():
            if tokens[i + 1] == '(' or tokens[i + 1].isalnum():
                tokens.insert(i + 1, '.')
        i += 1
    
    return tokens



# Usage example
# regex = "e|a*b"
regex = "The man|woman is"
postfix = regex_to_postfix(regex)
print(f"Regular Expression: {regex}")
print(f"Postfix Notation: {postfix}")

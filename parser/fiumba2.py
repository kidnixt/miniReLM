import re

def shunting_yard_regex(regex):
    output_queue = []
    operator_stack = []

    # Define the precedence of operators
    precedence = {'|': 1, '.': 2, '*': 3}

    for token in regex:
        if token.isalnum():
            # If the token is an operand (word), append it to the output queue
            output_queue.append(token)
        elif token == '(':
            # If the token is an opening parenthesis, push it onto the stack
            operator_stack.append(token)
        elif token == ')':
            # If the token is a closing parenthesis, pop operators from the stack to the output until an opening parenthesis is encountered
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            # Pop the opening parenthesis from the stack
            operator_stack.pop()
        else:
            # If the token is an operator, pop operators from the stack to the output while they have greater precedence or equal precedence and left-associativity
            while operator_stack and precedence.get(operator_stack[-1], 0) >= precedence.get(token, 0):
                output_queue.append(operator_stack.pop())
            # Push the current operator onto the stack
            operator_stack.append(token)

    # Pop any remaining operators from the stack to the output
    while operator_stack:
        output_queue.append(operator_stack.pop())

    return output_queue

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

# # Example usage
# regex = "The (man|woman) is"
# tokenized = tokenize_regex(regex)
# regex_words = ["The", ".", "(", "man", "|", "woman", ")", ".", "is"]
# postfix_result = shunting_yard_regex(regex_words)
# print("Posta:     ", postfix_result)
# print("Todo magia:", shunting_yard_regex(tokenized))
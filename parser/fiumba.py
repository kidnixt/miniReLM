def regex_to_postfix(regex):
    precedence = {'*': 3, '+': 3, '?': 3, '.': 2, '|': 1, '^': 0, '-': 0, '[': 0, ']': 0, '(': 0, ')': 0}  # Precedencia de operadores
    output = []  # Lista de salida (notación postfija)
    operator_stack = []  # Pila para operadores

    for char in regex:
        if char.isalnum():
            output.append(char)  # Agregar operandos directamente a la salida
        elif char == '[':
            operator_stack.append(char)
        elif char == ']':
            while operator_stack and operator_stack[-1] != '[':
                output.append(operator_stack.pop())
            operator_stack.pop()  # Eliminar '[' de la pila
        elif char == '(':
            operator_stack.append(char)
        elif char == ')':
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()  # Eliminar '(' de la pila
        else:
            # Procesamiento de operadores
            while operator_stack and precedence[char] <= precedence.get(operator_stack[-1], 0) and operator_stack[-1] != '(' and operator_stack[-1] != '[':
                output.append(operator_stack.pop())
            operator_stack.append(char)

    while operator_stack:
        output.append(operator_stack.pop())

    return ''.join(output)

# Ejemplo de uso
regex = "(e|(a)*b)"
postfix = regex_to_postfix(regex)
print(f"Expresión regular: {regex}")
print(f"Notación postfija: {postfix}")

from itertools import product

def read_file_to_string(file_path):
    """
    Legge un intero file e restituisce il contenuto come stringa.

    Args:
        file_path (str): Il percorso del file da leggere.

    Returns:
        str: Il contenuto del file come stringa.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Errore: Il file '{file_path}' non esiste.")
        return ""
    except IOError as e:
        print(f"Errore durante la lettura del file: {e}")
        return ""

def parse_line(line):
    """
    Parsea una singola linea del tipo "123123: 24 12 11 2".
    Restituisce un dizionario con:
    {
      "result": <numero a sinistra dei due punti come int>,
      "operands": <lista di interi sulla destra dei due punti>
    }
    """
    # Dividi la linea in due parti: prima e dopo i due punti
    left_part, right_part = line.split(":", 1)

    # Rimuovi spazi bianchi
    left_part = left_part.strip()
    right_part = right_part.strip()

    # Converti la parte a sinistra in int
    risultato = int(left_part)

    # Converti la parte a destra in una lista di interi
    operandi_str = right_part.split()
    operandi = [int(x) for x in operandi_str]

    return {
        "result": risultato,
        "operands": operandi
    }

def generate_combinations(N, symbols=None):
    """
    Genera tutte le combinazioni possibili di '+' e '*'
    di lunghezza N.
    Restituisce una lista di stringhe.
    """
    if symbols is None:
        symbols = ['+', '*']
    all_combinations = product(symbols, repeat=N)
    # all_combinations è un iteratore di tuple come ('+', '+', '*'), ecc.

    # Converti ogni tupla in stringa
    return [''.join(combo) for combo in all_combinations]

def combine_operands_and_operators(operands, operators):
    """
    Combina una lista di operandi e una lista di operatori in una stringa,
    supportando l'operatore '|'.
    Gli operatori devono essere almeno len(operands) - 1.

    Args:
        operands (list): Lista di numeri o stringhe (operandi).
        operators (list): Lista di stringhe (operatori, inclusi '|').

    Returns:
        str: Una stringa con operandi e operatori combinati.

    Raises:
        ValueError: Se il numero di operatori non è abbastanza per combinare gli operandi.
    """
    if len(operators) != len(operands) - 1:
        raise ValueError("Il numero di operatori deve essere pari a len(operands) - 1.")

    result = str(operands[0])  # Inizia con il primo operando

    for i in range(len(operators)):
        result += f"{operators[i]}{operands[i + 1]}"

    return result

def evaluate_in_order(operands, operators):
    """
    Valuta una sequenza di operandi e operatori da sinistra a destra,
    incluso l'operatore "|" per concatenare due numeri.

    Args:
        operands (list): Lista di numeri (int o float).
        operators (list): Lista di stringhe ('+', '-', '*', '/', '|').

    Returns:
        float: Il risultato dell'espressione calcolata in ordine.

    Raises:
        ValueError: Se il numero di operatori non è pari a len(operands) - 1.
    """
    if len(operators) != len(operands) - 1:
        raise ValueError("Il numero di operatori deve essere pari a len(operands) - 1.")

    result = operands[0]  # Inizia con il primo operando

    for i in range(len(operators)):
        operator = operators[i]
        operand = operands[i + 1]

        # Esegui l'operazione in base all'operatore
        if operator == '+':
            result += operand
        elif operator == '-':
            result -= operand
        elif operator == '*':
            result *= operand
        elif operator == '/':
            if operand == 0:
                raise ZeroDivisionError("Divisione per zero non consentita.")
            result /= operand
        elif operator == '|':
            # Concatena i due operandi come stringhe, poi converti in int
            result = int(f"{int(result)}{int(operand)}")
        else:
            raise ValueError(f"Operatore non valido: {operator}")

    return result

print("-----------------------------\nPART 1")

file_path = f"./inputs/07/input.txt"
file_content = read_file_to_string(file_path)

equation_list = [parse_line(l) for l in file_content.split('\n')]
#print(equation_list)
correct_equations = []

for equation_data in equation_list:
    result = equation_data["result"]
    operands = equation_data["operands"]
    print(f"result: {result} operands: {operands}")

    operations = generate_combinations(len(operands)-1,['+', '*'])
    print(operations)

    for possible_operations in operations:
        equation = combine_operands_and_operators(operands, possible_operations)
        real_result = evaluate_in_order(operands, possible_operations)
        print(f"equation: {equation} = {real_result}")

        if result == real_result and not correct_equations.__contains__(equation_data):
            print(f" > {equation} = {real_result} == {result} FOUND IT!!")
            correct_equations.append(equation_data)

print(f"\nSOLUTION --------------------")
sum = 0
for correct_equation in correct_equations:
    sum += correct_equation["result"]

print(f"solution: {sum}\n")

print("-----------------------------\nPART 2")

correct_equations = []

for equation_data in equation_list:
    result = equation_data["result"]
    operands = equation_data["operands"]
    print(f"result: {result} operands: {operands}")

    operations = generate_combinations(len(operands)-1,['+', '*', '|'])
    print(operations)

    for possible_operations in operations:
        equation = combine_operands_and_operators(operands, possible_operations)
        real_result = evaluate_in_order(operands, possible_operations)
        print(f"equation: {equation} = {real_result}")

        if result == real_result and not correct_equations.__contains__(equation_data):
            print(f" > {equation} = {real_result} == {result} FOUND IT!!")
            correct_equations.append(equation_data)

print(f"\nSOLUTION --------------------\n")
sum = 0
for correct_equation in correct_equations:
    sum += correct_equation["result"]

print(f"solution: {sum}\n")
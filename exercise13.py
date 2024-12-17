import re

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

def parse_input(input_string):
    """
    Estrae gli oggetti con le proprietà desiderate dal testo di input.

    Args:
        input_string (str): Il testo di input.

    Returns:
        list: Una lista di dizionari con le proprietà A, B e Prize.
    """
    # Regex per estrarre i dati
    button_pattern = r"Button (A|B): X\+(-?\d+), Y\+(-?\d+)"
    prize_pattern = r"Prize: X=(-?\d+), Y=(-?\d+)"

    # Suddividi l'input in sezioni
    sections = input_string.strip().split("\n\n")

    results = []

    for section in sections:
        # Trova tutte le corrispondenze per Button A e Button B
        buttons = re.findall(button_pattern, section)

        # Trova la corrispondenza per Prize
        prize = re.search(prize_pattern, section)

        if buttons and prize:
            obj = {
                "A": (int(buttons[0][1]), int(buttons[0][2])),
                "B": (int(buttons[1][1]), int(buttons[1][2])),
                "Prize": (int(prize.group(1)), int(prize.group(2)))
            }
            results.append(obj)

    return results


print("-----------------------------\nPART 1")


def find_combination(goal, step_a, step_b):
    max_a = goal // step_a
    results = []
    for passi_a in range(max_a, -1, -1):  # Partiamo da max_a e scendiamo
        resto = goal - (passi_a * step_a)
        if resto % step_b == 0:
            passi_b = resto // step_b
            results.append((passi_a, passi_b))
    return results


def find_steps_to_goal(prize, a_val, b_val):
    """
    Trova tutte le combinazioni di passi A e B per raggiungere il goal in X e Y.
    Testa sia partendo con A che con B.

    Args:
        prize (tuple): Coordinata (X, Y) del goal.
        a_val (tuple): Valori di incremento (X, Y) per il pulsante A.
        b_val (tuple): Valori di incremento (X, Y) per il pulsante B.

    Returns:
        dict: Dizionario con tutte le combinazioni trovate.
    """
    goal_x, goal_y = prize
    step_a_x, step_a_y = a_val
    step_b_x, step_b_y = b_val

    # Trova combinazioni per X e Y
    solutions = find_combination(goal_x, step_a_x, step_b_x)

    # Filtra solo soluzioni valide
    valid_solutions = []
    for x_a, x_b in solutions:
        if (x_a * step_a_x + x_b * step_b_x == goal_x) and (x_a * step_a_y + x_b * step_b_y == goal_y):
            valid_solutions.append({
                "steps": {"A": x_a, "B": x_b},
                "cost": x_a * 3 + x_b * 1
            })
    return valid_solutions


A_TOKEN = 3
B_TOKEN = 1

# file_path = f"./inputs/13/input.txt"
# file_content = read_file_to_string(file_path)
#
# machines = parse_input(file_content)
#
# print(f"machines: {machines}")
#
# total_cost = 0
#
# for machine in machines:
#     print(f"\n **** NEW MACHINE **** \n")
#     solutions = find_steps_to_goal(machine["Prize"], machine["A"], machine["B"])
#
#     if not solutions:
#         print("No valid solutions found!")
#         continue
#
#     print("Valid solutions:")
#     min_cost = float('inf')
#     best_solution = None
#
#     for solution in solutions:
#         x_steps_a = solution["steps"]["A"]
#         x_steps_b = solution["steps"]["B"]
#         cost = solution["cost"]
#
#         print(f"  -> Solution: {x_steps_a} steps A, {x_steps_b} steps B")
#         print(f"  -> Total Cost: {cost}")
#
#         if cost < min_cost:
#             min_cost = cost
#             best_solution = solution
#
#     if best_solution:
#         total_cost += best_solution['cost']
#
#         # Stampa la soluzione con il costo minimo
#         print("\nBest Solution:")
#         print(f"  -> Solution: {best_solution['steps']['A']} steps A, {best_solution['steps']['B']} steps B")
#         print(f"  -> Total Cost: {best_solution['cost']}")

print(f"\nSOLUTION --------------------\n")

# print(f"solution: {total_cost}\n")

print("-----------------------------\nPART 2")


def solve_linear_equations(a1, b1, c1, a2, b2, c2):
    """
    Risolve un sistema di due equazioni lineari a due incognite:
        a1*X + b1*Y = c1
        a2*X + b2*Y = c2

    Args:
        a1, b1, c1: Coefficienti della prima equazione.
        a2, b2, c2: Coefficienti della seconda equazione.

    Returns:
        tuple: Soluzioni (X, Y) se esistono, altrimenti None.
    """
    # Determinante del sistema
    determinant = (a1 * b2) - (a2 * b1)

    if determinant == 0:
        # Il sistema non ha soluzioni uniche (linee parallele o coincidenti)
        return None

    # Calcolo delle soluzioni
    X = (c1 * b2 - c2 * b1) / determinant
    Y = (a1 * c2 - a2 * c1) / determinant

    print(f"det: {determinant} X: {X} Y: {Y}")

    return X, Y


file_path = f"./inputs/13/input.txt"
file_content = read_file_to_string(file_path)

machines = parse_input(file_content)

print(f"machines: {machines}")

total_cost = 0

for machine in machines:
    print(f"\n **** NEW MACHINE **** \n")
    print(f"Goal: {machine['Prize']}, A: {machine['A']}, B: {machine['B']}")

    a1, a2 = machine["A"]  # Incrementi in X e Y per il pulsante A
    b1, b2 = machine["B"]  # Incrementi in X e Y per il pulsante B
    c1, c2 = machine["Prize"]  # Goal in X e Y
    c1 += 10000000000000
    c2 += 10000000000000

    print(a1, b1, c1)  # Coefficienti per l'equazione X
    print(a2, b2, c2)  # Coefficienti per l'equazione Y

    solutions = solve_linear_equations(a1, b1, c1, a2, b2, c2)

    # Controllo che X e Y siano interi
    if solutions:
        X, Y = solutions
        if X.is_integer() and Y.is_integer():  # Verifica che X e Y siano interi
            X, Y = int(X), int(Y)  # Converti a interi
            cost = X*3 + Y*1
            total_cost += cost
            print(f"Soluzioni: X = {X}, Y = {Y} @ cost = {cost}")
        else:
            print("Le soluzioni trovate non sono intere.")
    else:
        print("Il sistema non ha soluzioni uniche.")

print(f"\nSOLUTION --------------------\n")

print(f"solution: {total_cost}\n")

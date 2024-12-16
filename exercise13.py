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


# def follow_path_with_trails(current_pos, initial_pos, solutions, machine_data, n_steps, a_steps, b_steps):
#     goal = machine_data["Prize"]
#     a_val = machine_data["A"]
#     b_val = machine_data["B"]
#
#     if n_steps == 100 and current_pos != goal:
#         return solutions
#     elif n_steps <= 100 and current_pos == goal:
#         print(f" > found solution starting at {initial_pos} and ending at {current_pos}")
#         solution = {"start": initial_pos[0], "trails": initial_pos[1:], "end": current_pos, "A_steps": a_steps, "B_steps": b_steps}
#         if not solutions.__contains__(solution):
#             return solutions.append(solution)
#
#     directions = [
#         (a_val[0], a_val[1]),  # A
#         (b_val[0], b_val[1]),  # B
#     ]
#
#     for dr, dc in directions:
#         next_pos = (current_pos[0] + dr, current_pos[1] + dc)
#         if next_pos[0] > goal[0] or next_pos[1] > goal[1]:
#             continue
#         a_steps = a_steps + 1 if dc == a_val[1] else a_steps
#         b_steps = b_steps + 1 if dc == b_val[1] else b_steps
#
#         print(f"> next position {current_pos} => {next_pos}")
#
#         initial_pos.append(next_pos)
#         follow_path_with_trails(next_pos, initial_pos, solutions, goal, n_steps+1, a_val, b_val, a_steps, b_steps)
#
#     return solutions


def follow_path_with_trails(current_pos, initial_pos, solutions, machine_data, n_steps, a_steps, b_steps, visited=None):
    """
    Trova il percorso per raggiungere il goal (Prize) seguendo i percorsi A e B.

    Args:
        current_pos (tuple): Posizione corrente (X, Y).
        initial_pos (list): Lista delle posizioni visitate.
        solutions (list): Lista di soluzioni trovate.
        machine_data (dict): Dati della macchina con Prize, A, B.
        n_steps (int): Numero di passi effettuati.
        a_steps (int): Numero di passi fatti lungo il percorso A.
        b_steps (int): Numero di passi fatti lungo il percorso B.

    Returns:
        list: Lista delle soluzioni trovate.
    """
    if visited is None:
        visited = set()

    goal = machine_data["Prize"]
    a_val = machine_data["A"]
    b_val = machine_data["B"]

    print(f"Current position: {current_pos}")

    # Condizioni di uscita
    if n_steps == 100 and current_pos != goal:
        return solutions
    elif current_pos == goal:
        print(f"> Found solution starting at {initial_pos[0]} and ending at {current_pos}")
        solution = {
            "start": initial_pos[0],
            "trails": initial_pos[1:],  # Percorso completo
            "end": current_pos,
            "A_steps": a_steps,
            "B_steps": b_steps,
        }
        if solution not in solutions:
            solutions.append(solution)
        return solutions

    # Verifica se il percorso è già stato visitato
    state = (current_pos, a_steps, b_steps)
    if state in visited:
        print(f"!! Already visited {state}!!")
        return solutions
    visited.add(state)

    # Direzioni da esplorare
    directions = [
        (a_val[0], a_val[1], "A"),
        (b_val[0], b_val[1], "B"),
    ]

    for dr, dc, path_type in directions:
        next_pos = (current_pos[0] + dr, current_pos[1] + dc)

        # Ignora posizioni che superano il goal
        if next_pos[0] > goal[0] or next_pos[1] > goal[1]:
            continue

        # Aggiorna i passi A e B
        new_a_steps = a_steps + 1 if path_type == "A" else a_steps
        new_b_steps = b_steps + 1 if path_type == "B" else b_steps

        print(f"> Following path {path_type}: {current_pos} => {next_pos}")

        # Crea una nuova lista per evitare modifiche indesiderate
        new_initial_pos = initial_pos + [next_pos]

        # Chiamata ricorsiva
        follow_path_with_trails(next_pos, new_initial_pos, solutions, machine_data, n_steps + 1, new_a_steps, new_b_steps, visited)

    return solutions


A_TOKEN = 3
B_TOKEN = 1

file_path = f"./inputs/13/test.txt"
file_content = read_file_to_string(file_path)

machines = parse_input(file_content)

print(machines)

solutions = []
for machine in machines:
    starting_pos = (0, 0)
    follow_path_with_trails(starting_pos, [starting_pos], solutions, machine, 0, 0, 0)

print(solutions)

print(f"\nSOLUTION --------------------\n")

print(f"solution:\n")

print("-----------------------------\nPART 2")

print(f"\nSOLUTION --------------------\n")

print(f"solution:\n")

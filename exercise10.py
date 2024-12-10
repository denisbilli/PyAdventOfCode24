
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


def string_to_matrix(input_string):
    """
    Converte una stringa in una matrice XY di caratteri.
    Ogni riga è separata da un carattere di a capo '\n'.

    Args:
        input_string (str): La stringa da convertire.

    Returns:
        list: Matrice XY (lista di liste) di caratteri.
    """
    return [list(line) for line in input_string.splitlines()]


def get_matrix_dimensions(matrix):
    """
    Ottiene il numero di righe e colonne di una matrice.

    Args:
        matrix (list of list): Matrice rappresentata come una lista di liste.

    Returns:
        tuple: Numero di righe e numero di colonne (rows, cols).
    """
    rows = len(matrix)
    cols = len(matrix[0]) if matrix else 0  # Verifica che la matrice non sia vuota
    return rows, cols


def is_position_inside(matrix, guard_position):
    """
    Verifica se la posizione indicata da guard_position è all'interno della matrice.

    Args:
        matrix (list of list): La matrice di riferimento.
        guard_position (tuple): Tupla (row, col) che indica la posizione.

    Returns:
        bool: True se la posizione è all'interno della matrice, False altrimenti.
    """
    if not matrix:
        return False

    rows = len(matrix)
    cols = len(matrix[0])

    row, col = guard_position
    return 0 <= row < rows and 0 <= col < cols


def matrix_to_string(matrix):
    """
    Converte una matrice XY di caratteri in una stringa.
    Ogni riga della matrice corrisponde a una riga della stringa separata da '\n'.

    Args:
        matrix (list): Matrice XY (lista di liste) di caratteri.

    Returns:
        str: Stringa risultante.
    """
    return '\n'.join(''.join(row) for row in matrix)


def find_char_in_grid(grid, chars, known_positions=None):
    if known_positions is None:
        known_positions = []
    rows, cols = get_matrix_dimensions(grid)
    positions = []
    for row in range(rows):
        for col in range(cols):
            for char in chars:
                if grid[row][col] == char and not known_positions.__contains__((row, col)):
                    positions.append((row, col))
    return positions


print("-----------------------------\nPART 1")


def follow_path(grid, current_pos, initial_pos, solutions):
    element = int(grid[current_pos[0]][current_pos[1]])

    # Se troviamo il valore 9, il percorso è completo
    if element == 9:
        #print(f"> found solution starting at {initial_pos} and ending at {current_pos}")
        solution = {"start": initial_pos, "end": current_pos}
        if not solutions.__contains__(solution):
            return solutions.append(solution)

    # Direzioni di movimento (sx, su, dx, giu)
    directions = [
        (0, -1),  # sinistra
        (-1, 0),  # su
        (0, 1),  # destra
        (1, 0)  # giù
    ]

    for dr, dc in directions:
        next_pos = (current_pos[0] + dr, current_pos[1] + dc)

        # Verifica che la posizione successiva sia valida
        if is_position_inside(grid, next_pos):
            next_element = grid[next_pos[0]][next_pos[1]]
            if next_element != '.':
                next_element = int(next_element)
                if next_element == element + 1:
                    # Segui il percorso ricorsivamente
                    follow_path(grid, next_pos, initial_pos, solutions)

    return solutions


def follow_path_with_trails(grid, current_pos, initial_pos, solutions):
    element = int(grid[current_pos[0]][current_pos[1]])

    # Se troviamo il valore 9, il percorso è completo
    if element == 9:
        #print(f"> found solution starting at {initial_pos} and ending at {current_pos}")
        solution = {"start": initial_pos[0], "trails": initial_pos[1:], "end": current_pos}
        if not solutions.__contains__(solution):
            return solutions.append(solution)

    # Direzioni di movimento (sx, su, dx, giu)
    directions = [
        (0, -1),  # sinistra
        (-1, 0),  # su
        (0, 1),  # destra
        (1, 0)  # giù
    ]

    for dr, dc in directions:
        next_pos = (current_pos[0] + dr, current_pos[1] + dc)

        # Verifica che la posizione successiva sia valida
        if is_position_inside(grid, next_pos):
            next_element = grid[next_pos[0]][next_pos[1]]
            if next_element != '.':
                next_element = int(next_element)
                if next_element == element + 1:
                    initial_pos.append(next_pos)
                    # Segui il percorso ricorsivamente
                    follow_path_with_trails(grid, next_pos, initial_pos, solutions)

    return solutions


file_path = f"./inputs/10/input.txt"
file_content = read_file_to_string(file_path)

grid = string_to_matrix(file_content)

print(f"\ngrid:\n{matrix_to_string(grid)}")

starting_positions = find_char_in_grid(grid, ['0'])

print(f"\nstarting_positions: {starting_positions}")

solutions = []
for starting_pos in starting_positions:
    follow_path(grid, starting_pos, starting_pos, solutions)


print(solutions)

print(f"\nSOLUTION --------------------\n")

count = 0
checks = {}
for solution in solutions:
    if checks.keys().__contains__(solution["start"]):
        checks[solution["start"]].append(solution["end"])
    else:
        checks[solution["start"]] = [solution["end"]]
    count += 1


for solution in checks:
    print(f"solution: {solution} => {len(checks[solution])}")

print(f"final solution: {count}\n")

print("-----------------------------\nPART 2")

starting_positions = find_char_in_grid(grid, ['0'])

print(f"\nstarting_positions: {starting_positions}")

solutions = []
for starting_pos in starting_positions:
    follow_path_with_trails(grid, starting_pos, [starting_pos], solutions)


print(f"\nSOLUTION --------------------\n")

print(f"solution: {len(solutions)}\n")
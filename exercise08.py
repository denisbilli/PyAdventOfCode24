from itertools import combinations


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
    position = ()
    for row in range(rows):
        for col in range(cols):
            for char in chars:
                if grid[row][col] == char and not known_positions.__contains__((row, col)):
                    position = (row, col)
                    break
    return position


print("-----------------------------\nPART 1")


def find_relative_positions(pos1, pos2):
    """
    Trova due nuove posizioni basate sulla distanza relativa tra due posizioni date.

    Args:
        pos1 (tuple): La prima posizione (row, col).
        pos2 (tuple): La seconda posizione (row, col).

    Returns:
        list: Una lista contenente le due nuove posizioni.
    """
    row1, col1 = pos1
    row2, col2 = pos2

    # Calcola la distanza relativa
    delta_row = abs(row1 - row2)
    delta_col = abs(col1 - col2)

    # Determina la direzione della diagonale
    if (row1 < row2 and col1 < col2) or (row1 > row2 and col1 > col2):
        # Diagonale principale
        new_pos1 = (row1 - delta_row, col1 - delta_col)
        new_pos2 = (row2 + delta_row, col2 + delta_col)
    else:
        # Diagonale secondaria
        new_pos1 = (row1 - delta_row, col1 + delta_col)
        new_pos2 = (row2 + delta_row, col2 - delta_col)

    return [new_pos1, new_pos2]


file_path = f"./inputs/08/input.txt"
file_content = read_file_to_string(file_path)

grid = string_to_matrix(file_content)

print(matrix_to_string(grid))

antennas_positions = {}
antinode_positions = []

rows, cols = get_matrix_dimensions(grid)

# Trova le antenne e le loro frequenze uniche
for row in range(rows):
    for col in range(cols):
        item = grid[row][col]
        if item != '.':
            if item not in antennas_positions:
                # Aggiungi nuova antenna al dizionario
                antennas_positions[item] = [(row, col)]
            else:
                # Se l'antenna esiste già, aggiungi la nuova posizione alla lista
                antennas_positions[item].append((row, col))

print(f"\nantennas_positions: {antennas_positions}")

for antenna in antennas_positions:
    print(f"checking antenna {antenna}:")
    antenna_positions = antennas_positions[antenna]

    for pos1, pos2 in combinations(antenna_positions, 2):
        results = find_relative_positions(pos1, pos2)
        for result in results:
            if is_position_inside(grid, result) and not antinode_positions.__contains__(result):
                antinode_positions.append(result)

                if grid[result[0]][result[1]] == '.':
                    grid[result[0]][result[1]] = "#"

                print(matrix_to_string(grid))

print(f"\nSOLUTION --------------------\n")

print(matrix_to_string(grid))
print(antinode_positions)

print(f"solution: {len(antinode_positions)}\n")

print("-----------------------------\nPART 2")


def find_relative_positions_extended(grid, pos1, pos2, callback):
    """
    Trova più posizioni in entrambe le direzioni relative a due posizioni iniziali,
    continuando finché una funzione di callback restituisce True.

    Args:
        pos1 (tuple): La prima posizione (row, col).
        pos2 (tuple): La seconda posizione (row, col).
        callback (function): Funzione che accetta una posizione (row, col) e restituisce True o False.

    Returns:
        dict: Un dizionario con due chiavi:
              - "direction_1": lista di posizioni generate partendo da pos1.
              - "direction_2": lista di posizioni generate partendo da pos2.
    """
    row1, col1 = pos1
    row2, col2 = pos2

    # Calcola la distanza relativa
    delta_row = abs(row1 - row2)
    delta_col = abs(col1 - col2)

    # Determina la direzione della diagonale
    if (row1 < row2 and col1 < col2) or (row1 > row2 and col1 > col2):
        # Diagonale principale
        delta_row_sign = delta_row
        delta_col_sign = delta_col
    else:
        # Diagonale secondaria
        delta_row_sign = delta_row
        delta_col_sign = -delta_col

    results = []

    # Genera posizioni per direction_1 (partendo da pos1)
    current_pos = pos1
    while callback(grid, current_pos):
        results.append(current_pos)
        current_pos = (current_pos[0] - delta_row_sign, current_pos[1] - delta_col_sign)

    # Genera posizioni per direction_2 (partendo da pos2)
    current_pos = pos2
    while callback(grid, current_pos):
        results.append(current_pos)
        current_pos = (current_pos[0] + delta_row_sign, current_pos[1] + delta_col_sign)

    return results


for antenna in antennas_positions:
    print(f"checking antenna {antenna}:")
    antenna_positions = antennas_positions[antenna]

    for pos1, pos2 in combinations(antenna_positions, 2):
        results = find_relative_positions_extended(grid, pos1, pos2, is_position_inside)
        for result in results:
            if is_position_inside(grid, result) and not antinode_positions.__contains__(result):
                antinode_positions.append(result)

                if grid[result[0]][result[1]] == '.':
                    grid[result[0]][result[1]] = "#"

                print(matrix_to_string(grid))

print(f"\nSOLUTION --------------------\n")

print(matrix_to_string(grid))
print(antinode_positions)

print(f"solution: {len(antinode_positions)}\n")

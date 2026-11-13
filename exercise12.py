

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


print("-----------------------------\nPART 1")

file_path = f"./inputs/12/input.txt"
file_content = read_file_to_string(file_path)

grid = string_to_matrix(file_content)
rows, cols = get_matrix_dimensions(grid)


def calculate_perimeter(group, grid):
    """
    Calcola il perimetro di un gruppo di coordinate.
    Args:
        group (list of tuple): Lista di coordinate del gruppo corrente.
        grid (list of list): Griglia di riferimento.

    Returns:
        int: Perimetro del gruppo.
    """
    rows, cols = len(grid), len(grid[0])
    perimeter = 0

    for x, y in group:
        # Controlla ogni direzione (su, giù, sinistra, destra)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            # Se è fuori dalla griglia o è una cella vuota ('.'), conta come perimetro
            if not (0 <= nx < rows and 0 <= ny < cols) or grid[nx][ny] == ".":
                perimeter += 1
            # Se appartiene a un altro gruppo dello stesso elemento, conta come perimetro
            elif (nx, ny) not in group:
                perimeter += 1

    return perimeter


def find_adjacent_groups(grid):
    """
    Trova gruppi di coordinate adiacenti in una griglia.

    Args:
        grid (list of list): La griglia.

    Returns:
        dict: Dizionario con i gruppi identificati.
    """
    rows, cols = len(grid), len(grid[0])
    visited = set()
    groups = {}

    def dfs(r, c, element):
        stack = [(r, c)]
        group = []
        while stack:
            x, y = stack.pop()
            if (x, y) not in visited and grid[x][y] == element:
                visited.add((x, y))
                group.append((x, y))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if 0 <= x + dx < rows and 0 <= y + dy < cols:
                        stack.append((x + dx, y + dy))
        return group

    for r in range(rows):
        for c in range(cols):
            element = grid[r][c]
            if element != "." and (r, c) not in visited:
                group = dfs(r, c, element)
                if element not in groups:
                    groups[element] = []
                groups[element].append(group)

    return groups


# Trova i gruppi adiacenti
groups = find_adjacent_groups(grid)
total_price = 0

# Calcola il perimetro per ogni gruppo
print("Perimeters:")
for element, group_list in groups.items():
    for i, group in enumerate(group_list, start=1):
        area = len(group_list[i-1])
        perimeter = calculate_perimeter(group, grid)
        print(f"{element}_{i}: Perimeter = {perimeter} Area = {area} => Cost = {perimeter*area}")
        total_price += perimeter*area


print(f"\nSOLUTION --------------------\n")

print(f"solution: {total_price}\n")

print("-----------------------------\nPART 2")


def calculate_perimeter_from_corners(group, grid):
    """
    Calcola il perimetro di un gruppo basandosi sui cambi di direzione (angoli).

    Args:
        group (list of tuple): Lista di coordinate del gruppo corrente.
        grid (list of list): Griglia di riferimento.

    Returns:
        int: Numero totale di spigoli (angoli) del gruppo.
    """
    rows, cols = len(grid), len(grid[0])
    perimeter_corners = 0

    # Trova il bordo del gruppo
    def is_border(x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < rows and 0 <= ny < cols) or grid[nx][ny] == ".":
                return True
        return False

    # Ordina le coordinate del gruppo in modo che il percorso sia sequenziale
    def find_border_path(start):
        path = []
        visited = set()
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Su, destra, giù, sinistra

        def next_direction(x, y, prev_direction):
            for i, (dx, dy) in enumerate(directions):
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited and (nx, ny) in border_points:
                    return (nx, ny), (dx, dy)
            return None, prev_direction

        current = start
        prev_direction = None
        while current:
            path.append(current)
            visited.add(current)
            current, prev_direction = next_direction(*current, prev_direction)

        return path

    # Trova tutti i punti di bordo
    border_points = [point for point in group if is_border(*point)]

    # Costruisce il percorso del bordo
    if not border_points:
        return 0

    start_point = border_points[0]
    border_path = find_border_path(start_point)

    # Conta i cambi di direzione
    prev_direction = None
    for i in range(1, len(border_path)):
        x1, y1 = border_path[i - 1]
        x2, y2 = border_path[i]
        direction = (x2 - x1, y2 - y1)

        if prev_direction is not None and direction != prev_direction:
            perimeter_corners += 1
        prev_direction = direction

    # Aggiungi 4 spigoli finali per chiudere il gruppo
    return perimeter_corners + 4


file_path = f"./inputs/12/test1.txt"
file_content = read_file_to_string(file_path)

grid = string_to_matrix(file_content)
rows, cols = get_matrix_dimensions(grid)

# Trova i gruppi adiacenti
groups = find_adjacent_groups(grid)

print(groups)
total_price = 0

# Calcola il perimetro per ogni gruppo
print("Perimeters:")
for element, group_list in groups.items():
    for i, group in enumerate(group_list, start=1):
        area = len(group_list[i-1])
        perimeter = calculate_perimeter_from_corners(group, grid)
        print(f"{element}_{i}: Perimeter = {perimeter} Area = {area} => Cost = {perimeter*area}")
        total_price += perimeter*area

print(f"\nSOLUTION --------------------\n")

print(f"solution: {total_price}\n")
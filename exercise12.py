

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


def follow_path_with_trails(grid, current_pos, initial_pos, solutions):
    element = int(grid[current_pos[0]][current_pos[1]])
    initial_element = int(grid[initial_pos[0]][initial_pos[1]])

    # Se troviamo il valore 9, il percorso è completo
    if element != initial_element and current_pos in solutions:
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


# def find_adjacent_groups(coordinates):
#     """
#     Trova gruppi di coordinate adiacenti in una lista.
#
#     Args:
#         coordinates (list of tuple): Lista di coordinate (x, y).
#
#     Returns:
#         list of list of tuple: Lista di gruppi di coordinate adiacenti.
#     """
#     def are_adjacent(coord1, coord2):
#         """Verifica se due coordinate sono adiacenti."""
#         x1, y1 = coord1
#         x2, y2 = coord2
#         return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1
#
#     groups = []
#     visited = set()
#
#     for coord in coordinates:
#         if coord not in visited:
#             # Nuovo gruppo
#             group = []
#             to_visit = [coord]
#
#             while to_visit:
#                 current = to_visit.pop()
#                 if current not in visited:
#                     visited.add(current)
#                     group.append(current)
#                     # Aggiungi coordinate adiacenti non ancora visitate
#                     to_visit.extend(
#                         [neighbor for neighbor in coordinates if neighbor not in visited and are_adjacent(current, neighbor)]
#                     )
#
#             groups.append(group)
#
#     return groups
#
#
# def find_adjacent_groups_with_names(coordinates):
#     """
#     Trova gruppi di coordinate adiacenti in una lista e garantisce che ogni duplicato venga trattato separatamente.
#
#     Args:
#         coordinates (list of tuple): Lista di coordinate (x, y).
#
#     Returns:
#         list of list of tuple: Lista di gruppi di coordinate adiacenti.
#     """
#     def are_adjacent(coord1, coord2):
#         """Verifica se due coordinate sono adiacenti."""
#         x1, y1 = coord1
#         x2, y2 = coord2
#         return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1
#
#     groups = []
#     visited = set()
#     coordinate_counter = {}
#
#     for coord in coordinates:
#         # Gestione delle coordinate duplicate
#         if coord in coordinate_counter:
#             coordinate_counter[coord] += 1
#             coord = (coord[0], coord[1], coordinate_counter[coord])  # Rende unica la coordinata
#         else:
#             coordinate_counter[coord] = 1
#
#         if coord not in visited:
#             # Nuovo gruppo
#             group = []
#             to_visit = [coord]
#
#             while to_visit:
#                 current = to_visit.pop()
#                 if current not in visited:
#                     visited.add(current)
#                     group.append((current[0], current[1]))  # Ignora il conteggio aggiunto
#                     # Aggiungi coordinate adiacenti non ancora visitate
#                     to_visit.extend(
#                         [neighbor for neighbor in coordinates if neighbor not in visited and are_adjacent(current, neighbor)]
#                     )
#
#             groups.append(group)
#
#     return groups
#
#
# def calculate_perimeter(group):
#     """
#     Calcola il perimetro di un gruppo di elementi adiacenti.
#
#     Args:
#         group (list of tuple): Lista di coordinate (x, y) adiacenti.
#
#     Returns:
#         int: Il perimetro del gruppo.
#     """
#     def is_edge(coord, neighbors):
#         """Verifica se una data coordinata ha un lato esposto."""
#         x, y = coord
#         # Controlla le 4 direzioni
#         adjacent_positions = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
#         return sum(1 for pos in adjacent_positions if pos not in neighbors)
#
#     # Converti il gruppo in un set per velocizzare le operazioni
#     neighbor_set = set(group)
#     perimeter = 0
#
#     for coord in group:
#         # Conta i lati esposti per ogni elemento
#         perimeter += is_edge(coord, neighbor_set)
#
#     return perimeter


print("-----------------------------\nPART 1")

file_path = f"./inputs/12/input.txt"
file_content = read_file_to_string(file_path)

grid = string_to_matrix(file_content)
rows, cols = get_matrix_dimensions(grid)

# elements = {}
#
# for row in range(rows):
#     for col in range(cols):
#         element = grid[row][col]
#         if not elements.keys().__contains__(element):
#             elements[element] = [(row,col)]
#         else:
#             elements[element].append((row,col))
#
# #print(elements)
#
# for element in elements:
#     list = elements[element]
#     sublists = find_adjacent_groups_with_names(list)
#
#     elements[element] = sublists
#
# total_price = 0
# for element in elements:
#     for sublist in elements[element]:
#         area = len(sublist)
#         perimeter = calculate_perimeter(sublist)
#         price = area * perimeter
#         print(f"element: {element} area: {area} perimeter: {perimeter} price: {price}")
#         total_price += price

#print(elements)

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

print(f"\nSOLUTION --------------------\n")

print(f"solution:\n")

from file_utils import *
from matrix_utils import *
from string_utils import *


def get_positions_with_same_y(target_position, positions):
    """
    Restituisce tutti gli elementi della lista che hanno Y uguale a quello della posizione target.

    Args:
        target_position (tuple): La posizione target (X, Y).
        positions (list): La lista di posizioni [(X1, Y1), (X2, Y2), ...].

    Returns:
        list: Una lista di posizioni con lo stesso Y della posizione target.
    """
    target_y = target_position[1]
    return [pos for pos in positions if pos[1] == target_y]


def get_positions_with_same_x(target_position, positions):
    """
    Restituisce tutti gli elementi della lista che hanno Y uguale a quello della posizione target.

    Args:
        target_position (tuple): La posizione target (X, Y).
        positions (list): La lista di posizioni [(X1, Y1), (X2, Y2), ...].

    Returns:
        list: Una lista di posizioni con lo stesso Y della posizione target.
    """
    target_x = target_position[0]
    return [pos for pos in positions if pos[0] == target_x]


def all_elements_equal(input_list):
    """
    Verifica se tutti gli elementi di una lista sono uguali.

    Args:
        input_list (list): La lista di input.

    Returns:
        bool: True se tutti gli elementi sono uguali, False altrimenti.
    """
    if not input_list:
        return True  # Una lista vuota è considerata "tutti uguali"
    return all(element == input_list[0] for element in input_list)


def get_unique_elements(input_list):
    """
    Restituisce gli elementi univoci di una lista, mantenendo l'ordine.

    Args:
        input_list (list): La lista di input.

    Returns:
        list: Una lista contenente solo gli elementi univoci.
    """
    seen = set()
    unique_elements = []
    for item in input_list:
        if item not in seen:
            unique_elements.append(item)
            seen.add(item)
    return unique_elements


def find_connected_blocks(grid, start_pos, direction):
    """
    Trova tutti i blocchi validi connessi nella direzione specificata.

    Args:
        grid (list of list): La griglia di elementi.
        start_pos (tuple): La posizione iniziale (riga, colonna).
        direction (str): La direzione come stringa ('up', 'down').

    Returns:
        list: Una lista di tuple con le posizioni dei blocchi connessi.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Determina i delta in base alla direzione
    if direction == "up":
        dr, dc = -1, 0
    elif direction == "down":
        dr, dc = 1, 0
    else:
        raise ValueError("Direzione non valida. Usa 'up' o 'down'.")

    # Posizioni già visitate per evitare loop
    visited = set()
    blocks = []

    def dfs(r, c):
        """Ricerca in profondità per trovare blocchi connessi."""
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols):
            return
        if grid[r][c] != '[' and grid[r][c] != ']':
            return

        visited.add((r, c))

        # Aggiungi il blocco iniziale o connesso
        if grid[r][c] == '[':
            blocks.append((r, c))
        elif grid[r][c] == ']':
            blocks.append((r, c - 1))  # Trova la coppia '[' ']' a sinistra

        # Controlla il blocco sopra o sotto (in base alla direzione)
        dfs(r + dr, c)

        # Controlla blocchi adiacenti lateralmente
        if c > 0:
            dfs(r, c - 1)
        if c < cols - 1:
            dfs(r, c + 1)

    # Avvia la ricerca dal punto di partenza
    dfs(*start_pos)
    return blocks


def find_connected_blocks_quasi_ok(grid, start_pos, direction):
    """
    Trova tutti i blocchi validi connessi nella direzione specificata, con regole per casi limite.

    Args:
        grid (list of list): La griglia di elementi.
        start_pos (tuple): La posizione iniziale (riga, colonna).
        direction (str): La direzione come stringa ('up', 'down').

    Returns:
        list: Una lista di tuple con le posizioni dei blocchi connessi.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Determina i delta in base alla direzione
    if direction == "up":
        dr, dc = -1, 0
    elif direction == "down":
        dr, dc = 1, 0
    else:
        raise ValueError("Direzione non valida. Usa 'up' o 'down'.")

    visited = set()
    blocks = []

    def dfs(r, c, is_vertical_path=True):
        """Ricerca in profondità per trovare blocchi connessi."""
        # Se fuori dai limiti o già visitata, esci
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols):
            return
        # Se la cella non è un blocco, esci
        if grid[r][c] != '[' and grid[r][c] != ']':
            return

        visited.add((r, c))

        # Aggiungi il blocco iniziale o connesso
        if grid[r][c] == '[':
            blocks.append((r, c))
        elif grid[r][c] == ']':
            blocks.append((r, c - 1))  # Trova la coppia '[' ']' a sinistra

        # Controlla il blocco sopra o sotto nella stessa colonna
        dfs(r + dr, c, is_vertical_path=True)

        # Espansione laterale condizionata
        if is_vertical_path:
            if c > 0 and grid[r][c - 1] == ']' and grid[r][c] == '[':
                dfs(r, c - 1, is_vertical_path=False)
            if c < cols - 1 and grid[r][c + 1] == '[' and grid[r][c] == ']':
                dfs(r, c + 1, is_vertical_path=False)

    # Avvia la ricerca dal punto di partenza
    dfs(*start_pos)
    return blocks


def find_connected_blocks_5(grid, start_pos, direction):
    """
    Trova tutti i blocchi validi connessi nella direzione specificata, con regole per casi limite.

    Args:
        grid (list of list): La griglia di elementi.
        start_pos (tuple): La posizione iniziale (riga, colonna).
        direction (str): La direzione come stringa ('up', 'down').

    Returns:
        list: Una lista di tuple con le posizioni dei blocchi connessi.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Determina i delta in base alla direzione
    if direction == "up":
        dr, dc = -1, 0
    elif direction == "down":
        dr, dc = 1, 0
    else:
        raise ValueError("Direzione non valida. Usa 'up' o 'down'.")

    visited = set()
    blocks = []

    def dfs(r, c, is_vertical_path=True):
        """Ricerca in profondità per trovare blocchi connessi."""
        # Se fuori dai limiti o già visitata, esci
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols):
            return
        # Se la cella non è un blocco, esci
        if grid[r][c] != '[' and grid[r][c] != ']':
            return

        visited.add((r, c))

        # Aggiungi il blocco iniziale o connesso
        if grid[r][c] == '[':
            blocks.append((r, c))
        elif grid[r][c] == ']':
            blocks.append((r, c - 1))  # Trova la coppia '[' ']' a sinistra

        # Controlla il blocco sopra o sotto nella stessa colonna
        dfs(r + dr, c, is_vertical_path=True)

        # Espansione laterale condizionata
        if is_vertical_path:
            if c > 0 and grid[r][c - 1] == ']' and grid[r][c] == '[':
                dfs(r, c - 1, is_vertical_path=False)
            if c < cols - 1 and grid[r][c + 1] == '[' and grid[r][c] == ']':
                dfs(r, c + 1, is_vertical_path=False)

    # Avvia la ricerca dal punto di partenza
    dfs(*start_pos, is_vertical_path=True)
    return blocks


def find_connected_blocks_6(grid, start_pos, direction):
    """
    Trova tutti i blocchi validi connessi nella direzione specificata, con regole per casi limite.

    Args:
        grid (list of list): La griglia di elementi.
        start_pos (tuple): La posizione iniziale (riga, colonna).
        direction (str): La direzione come stringa ('up', 'down').

    Returns:
        list: Una lista di tuple con le posizioni dei blocchi connessi.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Determina i delta in base alla direzione
    if direction == "up":
        dr, dc = -1, 0
    elif direction == "down":
        dr, dc = 1, 0
    else:
        raise ValueError("Direzione non valida. Usa 'up' o 'down'.")

    visited = set()
    blocks = []

    def dfs(r, c, col_constraint):
        """Ricerca in profondità per trovare blocchi connessi."""
        # Se fuori dai limiti o già visitata, esci
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols):
            return
        # Se la cella non è un blocco, esci
        if grid[r][c] != '[' and grid[r][c] != ']':
            return

        visited.add((r, c))

        # Aggiungi il blocco iniziale o connesso
        if grid[r][c] == '[':
            blocks.append((r, c))
        elif grid[r][c] == ']':
            blocks.append((r, c - 1))  # Trova la coppia '[' ']' a sinistra

        # Controlla il blocco sopra o sotto nella stessa colonna
        dfs(r + dr, c, col_constraint)

        # Espansione laterale condizionata: verifica connessione verticale
        if c > 0 and grid[r][c - 1] == ']' and grid[r][c] == '[':
            if col_constraint == c - 1:  # Espansione laterale permessa solo nella colonna vincolata
                dfs(r, c - 1, col_constraint)
        if c < cols - 1 and grid[r][c + 1] == '[' and grid[r][c] == ']':
            if col_constraint == c + 1:  # Espansione laterale permessa solo nella colonna vincolata
                dfs(r, c + 1, col_constraint)

    # Avvia la ricerca dal punto di partenza
    dfs(start_pos[0] + dr, start_pos[1], col_constraint=start_pos[1])  # Limita alla colonna iniziale
    #dfs(start_pos[0] + dr, start_pos[1]+1, col_constraint=start_pos[1])  # Limita alla colonna iniziale
    return blocks



def find_extreme_position(positions, direction):
    """
    Trova la posizione estrema in base alla direzione fornita.

    Args:
        positions (list of tuples): Lista di posizioni (x, y).
        direction (str): Direzione ('up', 'down', 'left', 'right').

    Returns:
        tuple: La posizione estrema in base alla direzione.
    """
    if not positions:
        return None  # Nessuna posizione disponibile

    if direction == 'up':
        # Trova la posizione con il valore Y più piccolo (più in alto)
        return min(positions, key=lambda pos: (pos[1], pos[0]))  # In caso di parità, usa X
    elif direction == 'down':
        # Trova la posizione con il valore Y più grande (più in basso)
        return max(positions, key=lambda pos: (pos[1], pos[0]))  # In caso di parità, usa X
    elif direction == 'left':
        # Trova la posizione con il valore X più piccolo (più a sinistra)
        return min(positions, key=lambda pos: (pos[0], pos[1]))  # In caso di parità, usa Y
    elif direction == 'right':
        # Trova la posizione con il valore X più grande (più a destra)
        max_pos = max(positions, key=lambda pos: (pos[0], pos[1]))  # In caso di parità, usa Y
        return (max_pos[0], max_pos[1]+1)
    else:
        raise ValueError("Direzione non valida. Usa 'up', 'down', 'left', o 'right'.")


def move_contiguous_elements_double(grid, start_pos, direction):
    """
    Trova il blocco '[' ']' nella posizione start_pos
    e lo sposta di 1 posizione nella direzione specificata.

    Args:
        grid (list of list): La griglia di elementi.
        start_pos (tuple): La posizione iniziale (riga, colonna).
        direction (str): La direzione come stringa ('up', 'down', 'left', 'right').

    Returns:
        int: Il numero di blocchi spostati.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Determina i delta in base alla direzione
    if direction == "up":
        dr, dc = -1, 0
    elif direction == "down":
        dr, dc = 1, 0
    elif direction == "left":
        dr, dc = 0, -1
    elif direction == "right":
        dr, dc = 0, 1
    else:
        raise ValueError("Direzione non valida. Usa 'up', 'down', 'left' o 'right'.")

    r, c = start_pos

    # Trova tutti i blocchi validi contigui
    blocks = []
    repos_start = False

    if direction == "left" or direction == "right":
        check_pos = start_pos

        found_left = False
        found_right = False
        while (is_position_inside (grid, check_pos) and
               (grid[check_pos[0]][check_pos[1]] == '[' or grid[check_pos[0]][check_pos[1]] == ']')):
            if grid[check_pos[0]][check_pos[1]] == '[':
                if not found_right:
                    blocks.append(check_pos)
                    found_left = True
                else:
                    found_right = False
            elif grid[check_pos[0]][check_pos[1]] == ']':
                if not found_left:
                    blocks.append((check_pos[0], check_pos[1] - 1))
                    found_right = True
                else:
                    found_left = False
            check_pos = (check_pos[0] + dr, check_pos[1] + dc)
    else:
        # CASI 5-6-7
        start_pos_copy = start_pos
        next_pos = (start_pos[0]+dr, start_pos[1])
        if direction == "up":
            start_pos_copy = (start_pos[0] + 1, start_pos[1])
        else:
            start_pos_copy = (start_pos[0] - 1, start_pos[1])
        if grid[next_pos[0]][next_pos[1]] == ']':
            start_pos_copy = (start_pos[0], start_pos[1]-1)

        # check_pos = next_pos
        # last_found = grid[next_pos[0]][next_pos[1]]
        # for i in range(1, 3):
        #     check_pos = (check_pos[0]+dr, check_pos[1])
        #     cur_found = grid[check_pos[0]][check_pos[1]]
        #     if last_found != cur_found and (cur_found == '[' or cur_found == ']'):
        #         repos_start = True
        #         break

        blocks = get_unique_elements(find_connected_blocks_5(grid, start_pos, direction))

        # CASO 4
        # if repos_start:
        #     blocks = get_unique_elements(find_connected_blocks_quasi_ok(grid, start_pos, direction))

    available_movements = 0
    if direction == "left" or direction == "right":
        extreme_block = find_extreme_position(blocks, direction)
        cur_pos = (extreme_block[0] + dr, extreme_block[1] + dc)
        while is_position_inside(grid, cur_pos) and grid[cur_pos[0]][cur_pos[1]] == '.':
            cur_pos = (cur_pos[0] + dr, cur_pos[1] + dc)
            available_movements += 1
    else:
        extreme_block = find_extreme_position(blocks, direction)
        extreme_blocks = get_positions_with_same_x(extreme_block, blocks)
        block_movements = []
        idx = 0
        for block in reversed(extreme_blocks):
            cur_pos = (block[0] + dr, block[1] + dc)
            block_movements.append(0)
            while (is_position_inside(grid, cur_pos) and
                   grid[cur_pos[0]][cur_pos[1]] == '.' and
                   grid[cur_pos[0]][cur_pos[1]+1] == '.'):
                cur_pos = (cur_pos[0] + dr, cur_pos[1] + dc)
                block_movements[idx] += 1
            idx += 1

        available_movements = min(block_movements)

    if available_movements > 0:
        # Esegui lo spostamento
        for block in reversed(blocks):
            grid[block[0]][block[1]] = '.'
            grid[block[0]][block[1] + 1] = '.'
            new_block_l = (block[0] + dr, block[1] + dc)
            new_block_r = (block[0] + dr, block[1] + dc + 1)
            grid[new_block_l[0]][new_block_l[1]] = '['
            grid[new_block_r[0]][new_block_r[1]] = ']'

    return available_movements


def transform_grid(grid):
    """
    Trasforma la griglia di input in base alle regole specificate.

    Args:
        grid (list of list): La griglia di input.

    Returns:
        list of list: La nuova griglia trasformata.
    """
    # Definizione delle sostituzioni
    transformation_map = {
        '#': '##',
        'O': '[]',
        '.': '..',
        '@': '@.'
    }

    # Trasforma la griglia riga per riga
    new_grid = []
    for row in grid:
        new_row = ''.join(transformation_map[tile] for tile in row)
        new_grid.append(new_row)

    return new_grid


print("-----------------------------\nPART 1")

file_path = f"./inputs/15/input.txt"
file_content = read_file_to_string(file_path)

element_list = split_string_by_separator(file_content, '\n\n')
grid = string_to_matrix(element_list[0])
movements = [char for char in string_to_char_list(element_list[1]) if char != '\n']

robot_position = find_char_in_grid(grid, '@')

print(matrix_to_string(grid))

for movement in movements:
    direction = get_direction_from_char(movement)

    next_position = ()
    if direction == "up":
        next_position = (robot_position[0]-1, robot_position[1])
    elif direction == "left":
        next_position = (robot_position[0], robot_position[1]-1)
    elif direction == "right":
        next_position = (robot_position[0], robot_position[1]+1)
    elif direction == "down":
        next_position = (robot_position[0]+1, robot_position[1])

    is_obstructed = is_obstacle_in_line_to_position(grid, robot_position, direction, next_position)
    is_wall = grid[next_position[0]][next_position[1]] == '#'
    is_inside_grid = is_position_inside(grid, next_position)

    if is_wall:
        continue

    if is_inside_grid and not is_obstructed:
        move_element_in_matrix(grid, robot_position, next_position)
        robot_position = next_position
        #print(matrix_to_string(grid))
        continue

    if is_inside_grid and is_obstructed:
        moved_elements = move_contiguous_elements(grid, next_position, direction)
        if moved_elements > 0:
            move_element_in_matrix(grid, robot_position, next_position)
            robot_position = next_position
        #print(matrix_to_string(grid))
        continue

print(f"\nSOLUTION --------------------\n")

print(matrix_to_string(grid))
stores_positions = find_all_chars_in_grid(grid, 'O')

solution = 0

for position in stores_positions:
    solution += position[0]*100 + position[1]

print(f"solution: {solution}\n")

print("-----------------------------\nPART 2")

file_path = f"./inputs/15/test7.txt"
file_content = read_file_to_string(file_path)

element_list = split_string_by_separator(file_content, '\n\n')
grid = string_to_matrix(element_list[0])
if element_list[0].__contains__('O'):
    grid = transform_grid(grid)
movements = [char for char in string_to_char_list(element_list[1]) if char != '\n']

robot_position = find_char_in_grid(grid, '@')

print(matrix_to_string(grid))

for movement in movements:
    direction = get_direction_from_char(movement)

    next_position = ()
    if direction == "up":
        next_position = (robot_position[0]-1, robot_position[1])
    elif direction == "left":
        next_position = (robot_position[0], robot_position[1]-1)
    elif direction == "right":
        next_position = (robot_position[0], robot_position[1]+1)
    elif direction == "down":
        next_position = (robot_position[0]+1, robot_position[1])

    is_obstructed = is_obstacle_in_line_to_position(grid, robot_position, direction, next_position, ['[', ']'])
    is_wall = grid[next_position[0]][next_position[1]] == '#'
    is_inside_grid = is_position_inside(grid, next_position)

    print(f"\n Direction: {direction}\n")

    if is_wall:
        continue

    if is_inside_grid and not is_obstructed:
        move_element_in_matrix(grid, robot_position, next_position)
        robot_position = next_position
        print(matrix_to_string(grid))
        continue

    if is_inside_grid and is_obstructed:
        moved_elements = move_contiguous_elements_double(grid, next_position, direction)
        if moved_elements > 0:
            move_element_in_matrix(grid, robot_position, next_position)
            robot_position = next_position
        print(matrix_to_string(grid))
        continue

print(f"\nSOLUTION --------------------\n")

print(matrix_to_string(grid))
stores_positions = find_all_chars_in_grid(grid, '[')

solution = 0

for position in stores_positions:
    solution += position[0]*100 + position[1]

print(f"solution: {solution}\n")

# 1470397 too low

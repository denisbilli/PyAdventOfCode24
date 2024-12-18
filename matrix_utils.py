
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


def find_char_in_grid(grid, chars):
    rows, cols = get_matrix_dimensions(grid)
    position = ()
    for row in range(rows):
        for col in range(cols):
            for char in chars:
                if grid[row][col] == char:
                    position = (row, col)
                    break
    return position


def find_all_chars_in_grid(grid, chars, known_positions=None):
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


def get_direction_from_char(char):
    """
    Restituisce la direzione corrispondente a un carattere tra '^', '>', '<', 'v'.

    Args:
        char (str): Il carattere da analizzare.

    Returns:
        str or None: La direzione corrispondente ('up', 'down', 'left', 'right')
                     oppure None se il carattere non è riconosciuto.
    """
    mapping = {
        '^': 'up',
        'v': 'down',
        '<': 'left',
        '>': 'right'
    }
    return mapping.get(char, None)


def move_element_in_matrix(matrix, pos1, pos2):
    """
    Inserisce una 'X' nella posizione pos1 della matrice e sposta il carattere
    precedentemente presente in pos1 nella posizione pos2, se pos2 è all'interno della matrice.
    Se pos2 è fuori dalla matrice, il carattere di pos1 va perso.

    Args:
        matrix (list of list): La matrice di caratteri.
        pos1 (tuple): Posizione del primo elemento, es: (r, c).
        pos2 (tuple): Posizione del secondo elemento, es: (r, c).

    Returns:
        None: La matrice viene modificata inline.
    """
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0

    r1, c1 = pos1
    r2, c2 = pos2

    # Salva il carattere originale di pos1
    original_char = matrix[r1][c1]

    # Sostituisci pos1 con 'X'
    matrix[r1][c1] = '.'

    # Verifica se pos2 è interna alla matrice
    if 0 <= r2 < rows and 0 <= c2 < cols:
        # Se sì, posiziona il carattere originale di pos1 in pos2
        matrix[r2][c2] = original_char
    # Se pos2 è fuori dalla matrice, non facciamo nulla: il carattere originale va perso.


def move_contiguous_elements(grid, start_pos, direction):
    """
    Trova tutti gli elementi contigui 'O' in linea con la direzione a partire da start_pos
    e li sposta di 1 posizione nella direzione specificata.

    Args:
        grid (list of list): La griglia di elementi.
        start_pos (tuple): La posizione iniziale (riga, colonna).
        direction (str): La direzione come stringa ('up', 'down', 'left', 'right').

    Returns:
        list of list: La griglia aggiornata.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Determina i delta in base alla direzione
    if direction == "up":
        dr, dc = -1, 0
    elif direction == "left":
        dr, dc = 0, -1
    elif direction == "right":
        dr, dc = 0, 1
    elif direction == "down":
        dr, dc = 1, 0
    else:
        raise ValueError("Direzione non valida. Usa 'up', 'down', 'left' o 'right'.")

    r, c = start_pos

    # Trova tutti gli elementi 'O' contigui nella direzione
    contiguous_positions = []
    while 0 <= r < rows and 0 <= c < cols and grid[r][c] == 'O':
        contiguous_positions.append((r, c))
        r += dr
        c += dc

    # Verifica se il movimento è possibile (nessun muro e spazio vuoto nella direzione)
    for r, c in reversed(contiguous_positions):
        next_r = r + dr
        next_c = c + dc
        if not (0 <= next_r < rows and 0 <= next_c < cols) or grid[next_r][next_c] not in ['.', 'O']:
            # Se si incontra un muro '#' o si esce dalla griglia, il movimento si blocca
            return 0

    moved_elements = 0
    # Esegui lo spostamento
    for r, c in reversed(contiguous_positions):
        next_r = r + dr
        next_c = c + dc
        grid[next_r][next_c] = 'O'
        grid[r][c] = '.'
        moved_elements += 1

    return moved_elements


def is_obstacle_in_line_to_position(grid, start_pos, direction, target_pos):
    """
    Verifica se, nella linea retta a partire da start_pos nella direzione indicata,
    c'è un ostacolo 'O' prima di raggiungere target_pos.

    Args:
        grid (list of list of str): Griglia di caratteri.
        start_pos (tuple): (r, c) posizione di partenza.
        direction (str): Direzione tra '^', 'v', '<', '>'.
        target_pos (tuple): (r, c) posizione obiettivo.

    Returns:
        bool: True se c'è un ostacolo '#' prima di raggiungere target_pos, False altrimenti.
    """
    rows = len(grid)
    if rows == 0:
        return False
    cols = len(grid[0])

    r_start, c_start = start_pos
    r_target, c_target = target_pos

    if r_target > rows-1 or c_target > cols-1 or r_target < 0 or c_target < 0:
        return True
    if grid[r_target][c_target] == 'O':
        return True

    # Determina delta r, c e controlla l'allineamento del target nella direzione scelta
    if direction == 'up':
        if c_target != c_start or r_target >= r_start:
            return False
        dr, dc = -1, 0
    elif direction == 'down':
        if c_target != c_start or r_target <= r_start:
            return False
        dr, dc = 1, 0
    elif direction == 'left':
        if r_target != r_start or c_target >= c_start:
            return False
        dr, dc = 0, -1
    elif direction == 'right':
        if r_target != r_start or c_target <= c_start:
            return False
        dr, dc = 0, 1
    else:
        # Direzione non valida
        return False

    # Spostati lungo la linea dalla cella successiva a start_pos fino alla target_pos
    current_r = r_start + dr
    current_c = c_start + dc

    while 0 <= current_r < rows and 0 <= current_c < cols:
        if (current_r, current_c) == (r_target, c_target):
            # Raggiunto il target senza ostacoli
            return False
        if grid[current_r][current_c] == '#':
            # Ostacolo incontrato prima del target
            return True

        current_r += dr
        current_c += dc

    # Se esco dalla griglia prima di raggiungere il target, significa che non era sulla stessa linea direzionale.
    # Avendo già controllato l'allineamento, qui significa semplicemente che non c'è ostacolo lungo il percorso.
    return False


def create_matrix(rows, cols, default_value=0):
    """
    Crea una matrice NxM con un valore di default.

    Args:
        rows (int): Numero di righe (N).
        cols (int): Numero di colonne (M).
        default_value (optional): Valore di default per ogni elemento. Default è 0.

    Returns:
        list of list: Matrice NxM.
    """
    return [[default_value for _ in range(cols)] for _ in range(rows)]
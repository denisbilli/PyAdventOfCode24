import os
import time
from PIL import Image, ImageDraw, ImageFont

global_font = ImageFont.truetype("inputs/06/DejaVuSansMono.ttf", 16)

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
    matrix[r1][c1] = 'X'

    # Verifica se pos2 è interna alla matrice
    if 0 <= r2 < rows and 0 <= c2 < cols:
        # Se sì, posiziona il carattere originale di pos1 in pos2
        matrix[r2][c2] = original_char
    # Se pos2 è fuori dalla matrice, non facciamo nulla: il carattere originale va perso.

def rotate_direction_90(char):
    """
    Ruota di 90 gradi a destra la direzione indicata dal carattere.

    Args:
        char (str): Un carattere tra '^', '>', '<', 'v'.

    Returns:
        str: Il carattere corrispondente alla direzione ruotata di 90 gradi a destra.
             Restituisce None se il carattere non è valido.
    """
    mapping = {
        '^': '>',
        '>': 'v',
        'v': '<',
        '<': '^'
    }
    return mapping.get(char, None)

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

def text_to_image(text, font=global_font, padding=10, bg_color="white", text_color="black"):
    # Mappa di colori in base al carattere
    color_map = {
        ".": "gray",
        "#": "blue",
        "X": "red"
        # Aggiungi altri mapping se necessario
    }

    # Suddividi il testo in righe
    lines = text.split("\n")

    # Trova una linea non vuota o usa uno spazio
    non_empty_line = next((l for l in lines if l.strip()), " ")
    line_length = len(non_empty_line)

    # Misura un singolo carattere usando getbbox
    bbox = font.getbbox("X")
    char_width = bbox[2] - bbox[0]
    char_height = bbox[3] - bbox[1]

    # Calcola dimensioni finali
    max_line_width = char_width * line_length
    total_height = char_height * len(lines)

    img_width = max_line_width + padding * 2
    img_height = total_height + padding * 2

    # Crea l'immagine
    img = Image.new("RGB", (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(img)

    y_offset = padding
    for line in lines:
        x_offset = padding
        for ch in line:
            # Se il carattere è nella mappa, usa quel colore, altrimenti colore di default
            color = color_map.get(ch, text_color)
            draw.text((x_offset, y_offset), ch, font=font, fill=color)
            x_offset += char_width
        y_offset += char_height

    return img

def export_frame():
    img_path = f"inputs/06/frames/frame_{idx:04d}.png"
    if not os.path.exists(img_path):
        img = text_to_image(matrix_to_string(grid))
        img.save(img_path)


file_path = f"./inputs/06/input.txt"
file_content = read_file_to_string(file_path)

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


def initialize():
    grid = string_to_matrix(file_content)
    guard_position = find_char_in_grid(grid, ['^', '<', '>', 'v'])

    return grid, guard_position




# region PART 1

print("-----------------------------\nPART 1")

grid, guard_position = initialize()

idx = 0
while True:
    #export_frame()

    current_char = grid[guard_position[0]][guard_position[1]]
    direction = get_direction_from_char(current_char)

    next_position = ()
    if direction == "up":
        next_position = (guard_position[0]-1, guard_position[1])
    elif direction == "left":
        next_position = (guard_position[0], guard_position[1]-1)
    elif direction == "right":
        next_position = (guard_position[0], guard_position[1]+1)
    elif direction == "down":
        next_position = (guard_position[0]+1, guard_position[1])

    if not is_position_inside(grid, next_position):
        move_element_in_matrix(grid, guard_position, next_position)
        break

    other_elem = grid[next_position[0]][next_position[1]]

    if other_elem == "#":
        grid[guard_position[0]][guard_position[1]] = rotate_direction_90(current_char)
        continue
    elif other_elem == "." or other_elem == "X":
        move_element_in_matrix(grid, guard_position, next_position)
        guard_position = next_position

    idx += 1

#export_frame()

print(f"\n{matrix_to_string(grid)}")

print(f"\nSOLUTION --------------------\n")
positions_covered = matrix_to_string(grid).count('X')
print(f"result: {positions_covered}")

# endregion

print("-----------------------------\nPART 2")

def find_fourth_corner(pos1, pos2, pos3):
    """
    Dati tre punti (pos1, pos2, pos3), restituisce il quarto punto pos4 tale che
    la relazione tra pos1 e pos2 sia la stessa tra pos3 e pos4.

    Formulazione: pos4 = pos3 + (pos1 - pos2)

    Args:
        pos1, pos2, pos3 (tuple): coordinate (r, c) dei tre punti

    Returns:
        tuple: pos4 (r, c)
    """
    r1, c1 = pos1
    r2, c2 = pos2
    r3, c3 = pos3

    # Calcola il vettore (pos1 - pos2)
    delta_r = r1 - r2
    delta_c = c1 - c2

    # Applica il vettore a pos3
    r4 = r3 + delta_r
    c4 = c3 + delta_c

    return (r4, c4)

def is_obstacle_in_line_to_position(grid, start_pos, direction, target_pos):
    """
    Verifica se, nella linea retta a partire da start_pos nella direzione indicata,
    c'è un ostacolo '#' prima di raggiungere target_pos.

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
    if grid[r_target][c_target] == '#':
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

def find_horizontal_line_from_position(grid, start_pos):
    """
    Restituisce la linea orizzontale completa a partire da start_pos,
    estendendosi verso sinistra e verso destra finché non incontra un ostacolo o il bordo.

    Restituisce una tupla (r, c_min, c_max) dove:
      r = riga fissa
      c_min = colonna minima raggiunta
      c_max = colonna massima raggiunta
    """
    r_s, c_s = start_pos

    # Trova estremo a sinistra
    left_line = find_line_extreme(grid, start_pos, 'left')
    # Trova estremo a destra
    right_line = find_line_extreme(grid, start_pos, 'right')

    # left_line = (r_s, c_min_left, c_s) se si è mosso a sinistra
    # right_line = (r_s, c_s, c_max_right) se si è mosso a destra

    # Ora combiniamo i risultati
    # Se left_line o right_line è None significa che da quel lato non si è potuto andare (solo start_pos valida)
    if left_line is None and right_line is None:
        # Non ci si può muovere né a sinistra né a destra
        return (r_s, c_s, c_s)
    if left_line is None:
        # Solo destra disponibile
        r_line, c_min, c_max = right_line
        # c_min potrebbe essere c_s, quindi la linea parte esattamente dal punto di start_pos e va a destra
        return (r_line, c_min, c_max)
    if right_line is None:
        # Solo sinistra disponibile
        r_line, c_min, c_max = left_line
        # c_max potrebbe essere c_s, quindi la linea parte dal punto di start_pos e va a sinistra
        return (r_line, c_min, c_max)

    # Entrambe le linee disponibili
    # left_line = (r_s, c_min_left, c_s)
    # right_line = (r_s, c_s, c_max_right)
    # Combiniamo min e max
    _, c_min_left, _ = left_line
    _, _, c_max_right = right_line

    return (r_s, c_min_left, c_max_right)

def find_vertical_line_from_position(grid, start_pos):
    """
    Restituisce la linea verticale completa a partire da start_pos,
    estendendosi verso l'alto e verso il basso finché non incontra un ostacolo o il bordo.

    Restituisce una tupla (c, r_min, r_max) dove:
      c = colonna fissa
      r_min = riga minima raggiunta
      r_max = riga massima raggiunta
    """
    r_s, c_s = start_pos

    # Estremo verso l'alto
    up_line = find_line_extreme(grid, start_pos, 'up')
    # Estremo verso il basso
    down_line = find_line_extreme(grid, start_pos, 'down')

    # up_line = (c_s, r_min_up, r_s) se ci si è mossi in su
    # down_line = (c_s, r_s, r_max_down) se ci si è mossi in giù

    if up_line is None and down_line is None:
        # Non ci si può muovere né in su né in giù
        return (c_s, r_s, r_s)
    if up_line is None:
        # Solo giù disponibile
        c_line, r_min, r_max = down_line
        return (c_line, r_min, r_max)
    if down_line is None:
        # Solo su disponibile
        c_line, r_min, r_max = up_line
        return (c_line, r_min, r_max)

    # Entrambe disponibili
    # up_line = (c_s, r_min_up, r_s)
    # down_line = (c_s, r_s, r_max_down)
    _, r_min_up, _ = up_line
    _, _, r_max_down = down_line

    return (c_s, r_min_up, r_max_down)

def find_intersection_from_direction(grid, start_pos, direction):
    # Supponiamo di avere la funzione find_line_extreme già definita
    horizontal_line = find_horizontal_line_from_position(grid, (8, 6))
    vertical_line = find_vertical_line_from_position(grid, (8, 6))

    # Ora horizontal_line = (r_line, c_min, c_max)
    # e vertical_line = (c_line, r_min, r_max)

    # Se vogliamo l'intersezione:
    r_line, c_min, c_max = horizontal_line
    c_line, r_min, r_max = vertical_line

    if r_min <= r_line <= r_max and c_min <= c_line <= c_max:
        intersection = (r_line, c_line)

        # 5. Sposta l'intersezione di 1 cella nella direzione
        r_i, c_i = intersection
        if direction == 'up':
            intersection = (r_i - 1, c_i)
        elif direction == 'down':
            intersection = (r_i + 1, c_i)
        elif direction == 'left':
            intersection = (r_i, c_i - 1)
        elif direction == 'right':
            intersection = (r_i, c_i + 1)

        return intersection
    else:
        return None

def find_line_extreme(grid, start_pos, direction):
    """
    Trova l'estremo della linea di esplosione a partire da start_pos nella direzione indicata.
    La linea termina all'ostacolo '#' o al bordo della griglia.

    Returns:
      Se direzione è 'left' o 'right':
         (r_s, c_min, c_max)
      Se direzione è 'up' o 'down':
         (c_s, r_min, r_max)
    """
    rows = len(grid)
    if rows == 0:
        return None
    cols = len(grid[0])

    r_s, c_s = start_pos

    # Determina i delta
    if direction == 'up':
        dr, dc = -1, 0
    elif direction == 'down':
        dr, dc = 1, 0
    elif direction == 'left':
        dr, dc = 0, -1
    elif direction == 'right':
        dr, dc = 0, 1
    else:
        return None

    cur_r, cur_c = r_s, c_s
    # Avanza finché non incontri '#' o esci dalla griglia
    while True:
        next_r = cur_r + dr
        next_c = cur_c + dc
        if not (0 <= next_r < rows and 0 <= next_c < cols):
            # bordo raggiunto
            break
        if grid[next_r][next_c] == '#':
            # ostacolo trovato, fermati prima
            break
        # avanza
        cur_r, cur_c = next_r, next_c

    # Ora (cur_r, cur_c) è l'ultimo punto libero prima di un ostacolo/bordo
    if direction in ('left', 'right'):
        # linea orizzontale: r_s fisso, c_min = min(c_s, cur_c), c_max = max(c_s, cur_c)
        c_min = min(c_s, cur_c)
        c_max = max(c_s, cur_c)
        return (r_s, c_min, c_max)
    else:
        # linea verticale: c_s fisso, r_min = min(r_s, cur_r), r_max = max(r_s, cur_r)
        r_min = min(r_s, cur_r)
        r_max = max(r_s, cur_r)
        return (c_s, r_min, r_max)

def process_grid(grid, guard_position, direction):
    # Trova la linea orizzontale dalla guardia
    horizontal_line = find_horizontal_line_from_position(grid, guard_position)
    if horizontal_line is None:
        return []

    r_s, c_min, c_max = horizontal_line
    r_g, c_g = guard_position

    # Definisci il sotto-rettangolo
    # Supponiamo che la guardia sia sotto e guardi a sinistra, allora:
    # righe da 0 a r_s
    # colonne da c_min a c_max
    # Questa logica può variare a seconda del tuo scenario di gioco
    r_start = 0
    r_end = r_s
    found_intersections = []

    for r in range(r_start, r_end + 1):
        for c in range(c_min, c_max + 1):
            if grid[r][c] == '#':
                # trovato un '#' nella zona
                # Linea verticale: scende fino a r_s nella stessa colonna c
                # Intersezione: (r_s, c)
                intersection = (r_s, c)
                # Sposta di 1 cella nella direzione
                r_i, c_i = intersection
                if direction == 'up':
                    intersection = (r_i - 1, c_i)
                elif direction == 'down':
                    intersection = (r_i + 1, c_i)
                elif direction == 'left':
                    intersection = (r_i, c_i - 1)
                elif direction == 'right':
                    intersection = (r_i, c_i + 1)

                found_intersections.append(intersection)

    return found_intersections[0]

def iterate_free_positions(grid):
    """
    Generatore che, data una griglia (lista di liste),
    restituisce ad ogni chiamata (next) una posizione (r, c)
    in cui non è presente il carattere '#'.
    """
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val != '#':
                yield (r, c)

def is_sublist(list1, list2):
    n1, n2 = len(list1), len(list2)
    if n1 > n2:
        # Se list1 è più lunga di list2, non può essere contenuta
        return False

    for i in range(n2 - n1 + 1):
        # Controlla la sottolista di list2 di lunghezza n1 a partire da i
        if list2[i:i+n1] == list1:
            return True

    return False

def has_repeated_sublist_of_4(lst):
    """
    Verifica se nella lista lst esiste una sotto-lista contigua di 4 elementi
    che compare almeno due volte.
    Restituisce True se esiste, False altrimenti.
    """
    seen = set()
    length = len(lst)

    if length < 4:
        return False

    for i in range(length - 3):
        # Estrae il sotto-elenco di 4 elementi come una tupla (immutabile e hashabile)
        sub = tuple(lst[i:i+4])
        if sub in seen:
            # Questa sotto-lista di 4 elementi era già stata vista
            return True
        seen.add(sub)

    # Nessuna sotto-lista di 4 elementi compare almeno due volte
    return False

new_obstacles_put = []

solution_idx = 0
solutions_unchanged = 3

# while True:
#     grid, guard_position = initialize()
#
#     solution_found = False
#     direction_changes = 0
#     obstacles = []
#     print(f"\n{matrix_to_string(grid)}")
#
#     while True:
#         current_char = grid[guard_position[0]][guard_position[1]]
#         direction = get_direction_from_char(current_char)
#
#         if direction_changes > 2 and len(obstacles) > 2:
#             last = len(obstacles)
#             pos1 = obstacles[last-3]
#             pos2 = obstacles[last-2]
#             pos3 = obstacles[last-1]
#             pos4 = find_fourth_corner(pos1, pos2, pos3)
#
#             exists_o = find_char_in_grid(grid, 'O')
#
#             if not exists_o:
#                 has_obstacles = is_obstacle_in_line_to_position(grid, guard_position, direction, pos4)
#                 can_add_new_obstacle = not new_obstacles_put.__contains__(pos4) and not has_obstacles
#                 if can_add_new_obstacle:
#                     new_obstacles_put.append(pos4)
#
#                     grid[pos4[0]][pos4[1]] = "O"
#                     print(f"\n{matrix_to_string(grid)}")
#                     obstacles = []
#                     direction_changes = 0
#                 # else:
#                 #     edge_case_pos = process_grid(grid, guard_position, direction)
#                 #     if edge_case_pos:
#                 #         has_obstacles = is_obstacle_in_line_to_position(grid, guard_position, direction, edge_case_pos)
#                 #         can_add_new_obstacle = not new_obstacles_put.__contains__(edge_case_pos) and not has_obstacles
#                 #         if can_add_new_obstacle:
#                 #             new_obstacles_put.append(edge_case_pos)
#                 #
#                 #             grid[edge_case_pos[0]][edge_case_pos[1]] = "O"
#                 #             print(f"\n{matrix_to_string(grid)}")
#                 #             obstacles = []
#                 #             direction_changes = 0
#             elif exists_o:
#                 print(f"SOLUTION {solution_idx} FOUND !!")
#                 solution_idx += 1
#                 solution_found = True
#                 break
#
#         next_position = ()
#         if direction == "up":
#             next_position = (guard_position[0]-1, guard_position[1])
#         elif direction == "left":
#             next_position = (guard_position[0], guard_position[1]-1)
#         elif direction == "right":
#             next_position = (guard_position[0], guard_position[1]+1)
#         elif direction == "down":
#             next_position = (guard_position[0]+1, guard_position[1])
#
#         if not is_position_inside(grid, next_position):
#             move_element_in_matrix(grid, guard_position, next_position)
#             break
#
#         other_elem = grid[next_position[0]][next_position[1]]
#
#         if other_elem == "#" or other_elem == "O":
#             grid[guard_position[0]][guard_position[1]] = rotate_direction_90(current_char)
#             if other_elem == "#":
#                 obstacles.append(next_position)
#                 print(f"\n{matrix_to_string(grid)}")
#             direction_changes += 1
#             continue
#         elif other_elem == "." or other_elem == "X":
#             move_element_in_matrix(grid, guard_position, next_position)
#             guard_position = next_position
#
#     if not solution_found:
#         solutions_unchanged -= 1
#     if solutions_unchanged == 0:
#         break

posizioni = iterate_free_positions(grid)
pos = next(posizioni)
#pos = (5,84)
#pos = (6,3)

print("\n\nBRUTE FORCE MODE:")
while(pos):
    grid, guard_position = initialize()
    #print(f" > checking position: {pos} {grid[pos[0]][pos[1]]}")
    if pos in new_obstacles_put or grid[pos[0]][pos[1]] == '^':
        pos = next(posizioni)
        print(f" >> position already covered")
        continue
    else:
        solutions_unchanged = 1 # loop per 3 volte
        while True:
            grid, guard_position = initialize()
            grid[pos[0]][pos[1]] = 'O'

            loop_found = False
            direction_changes = 0
            obstacles = []
            prev_obstacles = []
            current_status = "moving"
            #print(f"\n{matrix_to_string(grid)}")

            while True:
                current_char = grid[guard_position[0]][guard_position[1]]
                direction = get_direction_from_char(current_char)

                if current_status == "rotated" and direction_changes > 3 and len(obstacles) > 3:
                    #print(f"\n{matrix_to_string(grid)}")
                    exists_o = find_char_in_grid(grid, 'O')

                    if exists_o and has_repeated_sublist_of_4(obstacles):
                        loop_found = True
                        break

                next_position = ()
                if direction == "up":
                    next_position = (guard_position[0]-1, guard_position[1])
                elif direction == "left":
                    next_position = (guard_position[0], guard_position[1]-1)
                elif direction == "right":
                    next_position = (guard_position[0], guard_position[1]+1)
                elif direction == "down":
                    next_position = (guard_position[0]+1, guard_position[1])

                if not is_position_inside(grid, next_position):
                    move_element_in_matrix(grid, guard_position, next_position)
                    break

                other_elem = grid[next_position[0]][next_position[1]]

                if other_elem == "#" or other_elem == "O":
                    grid[guard_position[0]][guard_position[1]] = rotate_direction_90(current_char)
                    obstacles.append(next_position)
                    #print(f"\n{matrix_to_string(grid)}")
                    current_status = "rotated"
                    direction_changes += 1
                    continue
                elif other_elem == "." or other_elem == "X":
                    move_element_in_matrix(grid, guard_position, next_position)
                    guard_position = next_position
                    current_status = "moving"
                    #print(f"\n{matrix_to_string(grid)}")

            if not loop_found:
                #print(f" > proceeding with next solution")
                break
            else:
                print(f"SOLUTION {solution_idx} FOUND !!")
                solution_idx += 1
                new_obstacles_put.append(pos)
                break
        try:
            pos = next(posizioni)
        except StopIteration:
            break

print(f"\nSOLUTION --------------------\n")

grid, _ = initialize()
for solution in new_obstacles_put:
    row = solution[0]
    col = solution[1]
    grid[row][col] = 'O'

print(matrix_to_string(grid))
print(f"\nsolutions: {solution_idx}")


from file_utils import *
from matrix_utils import *
from string_utils import *


print("-----------------------------\nPART 1")

file_path = f"./inputs/16/test.txt"
file_content = read_file_to_string(file_path)

grid = string_to_matrix(file_content)

start_position = find_char_in_grid(grid, ['S'])
end_position = find_char_in_grid(grid, ['E'])

def follow_guard_path(grid, guard_position):
    solutions = []
    visited_dirs = []
    """
    Segue il percorso di una guardia in una griglia, muovendola finché possibile
    nella direzione corrente e ruotando di 90° in senso orario quando incontra un ostacolo.

    Args:
        grid (list of list): Griglia che rappresenta l'ambiente.
        guard_position (tuple): Posizione iniziale della guardia.

    Returns:
        list of list: La griglia aggiornata.
    """
    def rotate_direction_90(char):
        """Ritorna il carattere associato alla rotazione di 90° in senso orario."""
        rotations = {
            "up": "right",
            "right": "down",
            "down": "left",
            "left": "up"
        }
        return rotations.get(char)

    def move_element_in_matrix(grid, old_pos, new_pos):
        """Sposta un elemento nella griglia da old_pos a new_pos."""
        grid[new_pos[0]][new_pos[1]] = grid[old_pos[0]][old_pos[1]]
        grid[old_pos[0]][old_pos[1]] = '.'

    def is_position_inside(grid, position):
        """Verifica se una posizione è valida all'interno della griglia."""
        rows, cols = len(grid), len(grid[0])
        r, c = position
        return 0 <= r < rows and 0 <= c < cols

    directions = ["up", "left", "right", "down"]

    for direction in directions:
        cur_dir = direction
        while True:
            current_char = grid[guard_position[0]][guard_position[1]]

            # Determina la posizione successiva
            if cur_dir == "up":
                next_position = (guard_position[0] - 1, guard_position[1])
            elif cur_dir == "left":
                next_position = (guard_position[0], guard_position[1] - 1)
            elif cur_dir == "right":
                next_position = (guard_position[0], guard_position[1] + 1)
            elif cur_dir == "down":
                next_position = (guard_position[0] + 1, guard_position[1])
            else:
                break  # Direzione sconosciuta

            # Controlla se la prossima posizione è valida
            if not is_position_inside(grid, next_position):
                break

            other_elem = grid[next_position[0]][next_position[1]]

            # Se trova un muro, ruota di 90° e continua
            if other_elem == "#":
                cur_dir = rotate_direction_90(cur_dir)
                continue

            # Se trova uno spazio vuoto o un obiettivo, si muove
            elif other_elem == ".":
                move_element_in_matrix(grid, guard_position, next_position)
                guard_position = next_position

            elif other_elem == "E":
                solutions.append(other_elem)

            print(matrix_to_string(grid))

    return solutions


result = follow_guard_path(grid, start_position)

# Stampa la griglia aggiornata
print(result)

print(f"\nSOLUTION --------------------\n")

print(f"solution: \n")

print("-----------------------------\nPART 2")


print(f"\nSOLUTION --------------------\n")

print(f"solution: \n")
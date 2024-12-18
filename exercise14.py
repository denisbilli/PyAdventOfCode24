import os

from file_utils import *
from matrix_utils import *
from string_utils import *
import re
from time import sleep


def parse_input(input_string):
    """
    Analizza l'input per estrarre informazioni sui robot.

    Args:
        input_string (str): Stringa di input formattata come 'p=x,y v=x,y'.

    Returns:
        list: Lista di dizionari con 'id', 'p' (posizione) e 'v' (velocità).
    """
    # Regex per estrarre i dati
    robot_pattern = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"

    # Trova tutte le corrispondenze
    robots = re.findall(robot_pattern, input_string)

    # Creazione dei risultati
    results = []
    for idx, robot in enumerate(robots):
        obj = {
            "id": idx + 1,
            "p": (int(robot[1]), int(robot[0])),
            "v": (int(robot[3]), int(robot[2]))
        }
        results.append(obj)

    return results


print("-----------------------------\nPART 1")


def calculate_final_position(p, v, S, N):
    """
    Calcola la posizione finale dopo N secondi in uno spazio con overlapping.

    Args:
        p (tuple): Posizione iniziale (p_x, p_y).
        v (tuple): Velocità (v_x, v_y).
        S (tuple): Dimensioni dello spazio (S_x, S_y).
        N (int): Numero di secondi.

    Returns:
        tuple: Posizione finale (p_x_final, p_y_final).
    """
    p_x, p_y = p
    v_x, v_y = v
    S_x, S_y = S

    # Calcola la posizione finale per X
    p_x_final = (p_x + N * v_x) % S_x
    if p_x_final < 0:
        p_x_final += S_x

    # Calcola la posizione finale per Y
    p_y_final = (p_y + N * v_y) % S_y
    if p_y_final < 0:
        p_y_final += S_y

    return p_x_final, p_y_final


def create_quadrants(S):
    """
    Crea i 4 quadranti della griglia, escludendo la riga e la colonna centrali.

    Args:
        S (tuple): Dimensioni della griglia (rows, cols).

    Returns:
        dict: Dizionario con i limiti di ciascun quadrante.
    """
    rows, cols = S
    midX = rows // 2
    midY = cols // 2

    quadrants = {
        "Q1": [(0, midX), (0, midY)],  # Alto sinistra
        "Q2": [(0, midX), (midY + 1, cols)],  # Alto destra
        "Q3": [(midX + 1, rows), (0, midY)],  # Basso sinistra
        "Q4": [(midX + 1, rows), (midY + 1, cols)],  # Basso destra
    }

    return quadrants


file_path = f"./inputs/14/input.txt"
file_content = read_file_to_string(file_path)

robots = parse_input(file_content)

S = (103, 101)
#S = (7, 11)
grid = create_matrix(S[0], S[1], '.')
quadrants = create_quadrants(S)

quadrant_robots = {q: [] for q in quadrants}

for robot in robots:
    final_position = calculate_final_position(robot["p"], robot["v"], S, 100)

    # Determina il quadrante
    for q_name, ((min_x, max_x), (min_y, max_y)) in quadrants.items():
        if min_x <= final_position[0] < max_x and min_y <= final_position[1] < max_y:
            quadrant_robots[q_name].append(robot)
            break

    if grid[final_position[0]][final_position[1]] == '.':
        grid[final_position[0]][final_position[1]] = '1'
    else:
        grid[final_position[0]][final_position[1]] = str(int(grid[final_position[0]][final_position[1]])+1)

print(matrix_to_string(grid))

solution = 1
for q_name, robots in quadrant_robots.items():
    print(f"Quadrante {q_name}: {len(robots)} robot")
    solution *= len(robots)

print(f"\nSOLUTION --------------------\n")

print(f"solution: {solution}\n")

print("-----------------------------\nPART 2")

def is_exit_condition_met(grid, n=8):
    for row in grid:
        consecutive_count = 0
        for cell in row:
            if cell == 'X':
                consecutive_count += 1
                if consecutive_count >= n:
                    return True
            else:
                consecutive_count = 0
    return False


robots = parse_input(file_content)

S = (103, 101)
N = 1

while True:
    grid = create_matrix(S[0], S[1], '.')
    print(f"> Trying {N}")
    for robot in robots:
        final_position = calculate_final_position(robot["p"], robot["v"], S, N)

        if grid[final_position[0]][final_position[1]] == '.':
            grid[final_position[0]][final_position[1]] = 'X'

    # Verifica la condizione di uscita
    if is_exit_condition_met(grid):
        print(f"\n\nSolution found at step {N}!")
        print(matrix_to_string(grid))
        break

    N += 1

print(f"\nSOLUTION --------------------\n")

print(f"solution: \n")

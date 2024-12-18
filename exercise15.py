
from file_utils import *
from matrix_utils import *
from string_utils import *


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


print(f"\nSOLUTION --------------------\n")

print(f"solution: \n")
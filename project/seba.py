# /**************************************************************************
#
#  File:        seba.py
#  Copyright:   (c) 2023 EvoPath Team
#  Description:
#  Designed by: Sebastian Pitica
#
#  Module-History:
#  Date        Author                Reason
#  24.11.2023  Sebastian Pitica      Basic structure and Wilson algorithm for maze gen (improved version from https://github.com/antigones/pymazes/blob/main/wilson.py)
#
#  **************************************************************************/

import numpy as np
import random as rd

NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4
NULL_DIRECTION = 0
PATH = ' '
WALL = '#'
VISITED = 1
STEP = 1


def wilson(size: int) -> np.ndarray:
    np.random.seed(42)
    matrix = np.zeros(shape=(size, size))
    MIN_COORD = 0
    MAX_COORD = size - 1
    maze = np.full([2 * size + 1, 2 * size + 1], WALL, dtype=str)
    cell_number = size * size

    i_coord = rd.randrange(size)
    j_coord = rd.randrange(size)
    matrix[i_coord, j_coord] = 1
    visited = [[i_coord, j_coord]]
    visited_from = [NULL_DIRECTION]

    while np.count_nonzero(matrix) < cell_number:
        if matrix[i_coord, j_coord] == VISITED:
            for i_coord in range(len(visited)):
                visited_i, visited_j = visited[i_coord]
                matrix[visited_i, visited_j] = VISITED
                maze_i = 2 * visited_i + 1
                maze_j = 2 * visited_j + 1
                maze[maze_i, maze_j] = PATH
                visited_from_direction = visited_from[i_coord]
                if visited_from_direction == NULL_DIRECTION:
                    continue
                if visited_from_direction == NORTH:
                    maze[maze_i - 1, maze_j] = PATH
                elif visited_from_direction == EAST:
                    maze[maze_i, maze_j + 1] = PATH
                elif visited_from_direction == SOUTH:
                    maze[maze_i + 1, maze_j] = PATH
                elif visited_from_direction == WEST:
                    maze[maze_i, maze_j - 1] = PATH

            visited.clear()
            visited_from.clear()
            i_coord = rd.randrange(size)
            j_coord = rd.randrange(size)
            visited.append([i_coord, j_coord])
            visited_from.append(NULL_DIRECTION)

        else:
            if [i_coord, j_coord] in visited:
                visited.clear()
                visited_from.clear()

            visited.append([i_coord, j_coord])
            can_go = [i_coord > MIN_COORD, j_coord < MAX_COORD, i_coord < MAX_COORD, j_coord > MIN_COORD]
            neighbour_direction = np.random.choice(np.nonzero(can_go)[0]) + 1
            visited_from.append(neighbour_direction)
            if neighbour_direction == NORTH:
                i_coord -= STEP
            elif neighbour_direction == EAST:
                j_coord += STEP
            elif neighbour_direction == SOUTH:
                i_coord += STEP
            elif neighbour_direction == WEST:
                j_coord -= STEP

    start_i_coord = 2 * rd.randrange(size) + 1
    star_j_coord = MIN_COORD
    finish_i_coord = 2 * rd.randrange(size) + 1
    finish_j_coord = 2 * MAX_COORD + 2

    while maze[start_i_coord, star_j_coord + 1] != PATH:
        start_i_coord = 2 * rd.randrange(size) + 1

    while maze[finish_i_coord, finish_j_coord - 1] != PATH:
        finish_i_coord = 2 * rd.randrange(size) + 1

    maze[start_i_coord, star_j_coord] = PATH
    maze[finish_i_coord, finish_j_coord] = PATH

    return maze

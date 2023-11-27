# /**************************************************************************
#
#  File:        matei.py
#  Copyright:   (c) 2023 EvoPath Team
#  Description:
#  Designed by: Matei Rares
#
#  Module-History:
#  Date        Author                Reason
#  24.11.2023  Matei Rares          Basic structure and functions
#  27.11.2023  Pitica Sebastian     Updated gen_pathway, todos and imports
#  27.11.2023  Matei Rares          Updated name variables and gen_adaptable_pathway(), deleted comments
#  **************************************************************************/

import random
from general_use import maze, MAZE_START, MAZE_END, MAZE_SIZE
from seba import PATH, WALL

RIGHT = "right"
LEFT = "left"
UP = "up"
DOWN = "down"
UNBLOCK = "unblock"
DIRECTIONS = [RIGHT, LEFT, UP, DOWN]
LIMIT_SUP_RIGHT_ANGLE = 45
LIMIT_INF_RIGHT_ANGLE = 315
LIMIT_SUP_LEFT_ANGLE = 225
LIMIT_INF_LEFT_ANGLE = 135
LIMIT_SUP_UP_ANGLE = 135
LIMIT_INF_UP_ANGLE = 45
LIMIT_SUP_DOWN_ANGLE = 315
LIMIT_INF_DOWN_ANGLE = 225


def gen_rand_angle():
    return random.uniform(0, 360)


# todo maybe will not be needed
def gen_nr_genes(maze_size):
    return random.randint(2 * maze_size, maze_size * maze_size)


def gen_individual(nr_genes):
    individual = []
    for i in range(0, nr_genes):
        individual.append(gen_rand_angle())
    return individual


def gen_population(nr_genes, nr_indivizi):
    population = []
    for i in range(0, nr_indivizi):
        population.append(gen_individual(nr_genes))
    return population


def det_direction(angle):
    if angle > LIMIT_INF_RIGHT_ANGLE or angle < LIMIT_SUP_RIGHT_ANGLE:
        return RIGHT
    elif LIMIT_INF_UP_ANGLE < angle < LIMIT_SUP_UP_ANGLE:
        return UP
    elif LIMIT_INF_LEFT_ANGLE < angle < LIMIT_SUP_LEFT_ANGLE:
        return LEFT
    elif LIMIT_INF_DOWN_ANGLE < angle < LIMIT_SUP_DOWN_ANGLE:
        return DOWN


def det_angle_based_on(direction):
    if direction == RIGHT:
        return 0
    elif direction == LEFT:
        return 180
    elif direction == UP:
        return 90
    elif direction == DOWN:
        return 270


def get_rand_dir_different_from(last_tried_dir):
    lista = [direct for direct in DIRECTIONS if direct not in last_tried_dir]
    if lista:
        return lista[random.randint(0, len(lista) - 1)]
    else:
        return UNBLOCK


def gen_adaptable_pathway(individual):
    pathway = []
    coord = MAZE_START
    pathway.append(coord)

    last_tried_dir = []
    coming_direction = None
    for i in range(len(individual)):
        gen = individual[i]
        direction = det_direction(gen)
        row, col = coord
        if direction in last_tried_dir:
            temp_dir = get_rand_dir_different_from(last_tried_dir)
            if temp_dir != UNBLOCK:
                direction = temp_dir
            else:
                direction = coming_direction

        if direction == RIGHT:
            if col + 1 == MAZE_SIZE:
                break
            if maze[row][col + 1] == PATH:
                col += 1
                last_tried_dir = [LEFT]
                coming_direction = LEFT
                individual[i-(len(last_tried_dir))]=det_angle_based_on(direction)

            elif maze[row][col + 1] == WALL:
                last_tried_dir.append(RIGHT)

        elif direction == LEFT:
            if col - 1 >= 0:
                last_tried_dir.append(LEFT)
            elif maze[row][col - 1] == PATH:
                col -= 1
                last_tried_dir = [RIGHT]
                coming_direction = RIGHT
                individual[i-(len(last_tried_dir))]=det_angle_based_on(direction)

            elif maze[row][col - 1] == WALL:
                last_tried_dir.append(LEFT)
        elif direction == UP:
            if maze[row - 1][col] == PATH:
                row -= 1
                last_tried_dir = [DOWN]
                coming_direction = DOWN
                individual[i-(len(last_tried_dir))]=det_angle_based_on(direction)

            elif maze[row - 1][col] == WALL:
                last_tried_dir.append(UP)
        elif direction == DOWN:
            if maze[row + 1][col] == PATH:
                row += 1
                last_tried_dir = [UP]
                coming_direction = UP
                individual[i-(len(last_tried_dir))]=det_angle_based_on(direction)

            elif maze[row + 1][col] == WALL:
                last_tried_dir.append(DOWN)

        coord = (row, col)
        pathway.append(coord)

    return pathway, individual

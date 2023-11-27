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
#  27.11.2023  Sebastian Pitica      Added particle swarm optimization algorithm lb and gb, added fitness func, added manhattan distance func, added eliminate duplicate neighbors func
#
#  **************************************************************************/

import numpy as np
import random as rd
from general_use import MAZE_SIZE, MAZE_END
from matei import gen_adaptable_pathway, gen_population, gen_individ

NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4
NULL_DIRECTION = 0
PATH = ' '
WALL = '#'
VISITED = 1
STEP = 1


def manhattan_distance_to_finish(start: tuple) -> int:
    return abs(start[0] - MAZE_END[0]) + abs(start[1] - MAZE_END[1])


def eliminate_duplicate_neighbors(input_list: list) -> list:
    result = []
    i = 0
    while i < len(input_list):
        current_tuple = input_list[i]
        result.append(current_tuple)
        j = i + 1
        while j < len(input_list) and current_tuple == input_list[j]:
            j += 1

        i = j

    print(str(input_list) + "\n" + str(result))  # todo remove
    return result


def adaptable_fitness_function(individual: list) -> (float, list):
    route, individual = gen_adaptable_pathway(individual)
    total_steps_count = len(route)
    unique_steps_count = len(eliminate_duplicate_neighbors(route))
    had_finished = (route[-1] == MAZE_END)
    remaining_distance = manhattan_distance_to_finish(route[-1])
    duplicate_steps_penalty = total_steps_count - unique_steps_count

    # The fitness function is a linear combination of the following:
    # - The number of unique steps taken to reach the finish (the less, the better)
    # - The remaining distance to the finish (the less, the better)
    # - The number of duplicate steps taken (the less, the better)

    # Fitness calculation formula:
    fitness_value = (
            ((1.0 / unique_steps_count) * MAZE_SIZE * 100 if had_finished else 0)  # Unique steps component
            - (remaining_distance * 10)  # Remaining distance component
            - (duplicate_steps_penalty * 5)  # Duplicate steps component
    )
    # The fitness value will be higher for solutions that take fewer unique steps, have less remaining distance,
    # and fewer duplicate steps.

    return fitness_value, individual


def particle_swarm_optimization_gbest(population: list, generations: int, consts: dict) -> list:
    population_length = len(population)
    nr_genes = len(population[0])

    speeds: list[list] = [gen_individ(len(population[0])) for _ in range(population_length)]
    personal_bests: list[list] = [population[i] for i in range(0, population_length)]
    fitness_personal_bests: list = [0 for _ in range(population_length)]

    global_best: list = population[0]
    fitness_global_best, global_best = adaptable_fitness_function(global_best)

    for _ in range(0, generations):
        for i in range(0, population_length):
            xi: list = population[i]
            vi: list = speeds[i]
            personal_best: list = personal_bests[i]
            fitness_personal_best: int = fitness_personal_bests[i]
            ###########################################################################

            fitness, xi = adaptable_fitness_function(xi)

            if fitness > fitness_personal_best:
                personal_best, fitness_personal_best = xi, fitness

            if fitness_personal_bests > fitness_global_best:
                global_best, fitness_global_best = personal_best, fitness_personal_bests

            vi = [(consts['w'] * vi[j] +
                   consts['c1'] * consts['r1'] * (personal_best[j] - xi[j]) +
                   consts['c2'] * consts['r2'] * (global_best[j] - xi[j]))
                  for j in range(0, nr_genes)]

            xi = xi + vi

            ###########################################################################
            population[i] = xi
            speeds[i] = vi
            personal_bests[i] = personal_best
            fitness_personal_bests[i] = fitness_personal_best

    return global_best


def particle_swarm_optimization_lbest(population: list, generations: int, consts: dict) -> list:
    population_length = len(population)
    nr_genes = len(population[0])

    local_bests = [population[0], population[0]]
    fitness_local_bests = list()
    fitness_local_bests[0], local_bests[0] = adaptable_fitness_function(local_bests[0])
    fitness_local_bests[1], local_bests[1] = adaptable_fitness_function(local_bests[1])

    speeds: list[list] = [gen_individ(len(population[0])) for _ in range(population_length)]
    personal_bests: list[list] = [population[i] for i in range(0, population_length)]
    fitness_personal_bests: list = [0 for _ in range(population_length)]

    for _ in range(0, generations):
        for i in range(0, population_length):
            xi: list = population[i]
            vi: list = speeds[i]
            personal_best: list = personal_bests[i]
            fitness_personal_best: int = fitness_personal_bests[i]
            local_best = local_bests[i % 2]
            fitness_local_best = fitness_local_bests[i % 2]
            ###########################################################################

            fitness, xi = adaptable_fitness_function(xi)

            if fitness > fitness_personal_best:
                personal_best, fitness_personal_best = xi, fitness

            if fitness_personal_bests > fitness_local_best:
                local_best, fitness_local_best = personal_best, fitness_personal_bests

            vi = [(consts['w'] * vi[j] +
                   consts['c1'] * consts['r1'] * (personal_best[j] - xi[j]) +
                   consts['c2'] * consts['r2'] * (local_best[j] - xi[j]))
                  for j in range(0, nr_genes)]

            xi = xi + vi

            ###########################################################################
            population[i] = xi
            speeds[i] = vi
            personal_bests[i] = personal_best
            fitness_personal_bests[i] = fitness_personal_best
            local_bests[i % 2] = local_best
            fitness_local_bests[i % 2] = fitness_local_best

    return local_bests


def particle_swarm_optimization(population_length: int, nr_genes: int, generations: int,
                                consts: dict):
    population = gen_population(nr_genes, population_length)
    gbest = particle_swarm_optimization_gbest(population, generations, consts)
    lbest = particle_swarm_optimization_lbest(population, generations, consts)


def gen_maze_wilson(size_factor: int) -> (np.ndarray, int, tuple, tuple):
    np.random.seed(42)
    matrix = np.zeros(shape=(size_factor, size_factor))
    min_coord = 0
    max_coord = size_factor - 1
    maze = np.full([2 * size_factor + 1, 2 * size_factor + 1], WALL, dtype=str)
    cell_number = size_factor * size_factor

    i_coord = rd.randrange(size_factor)
    j_coord = rd.randrange(size_factor)
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
            i_coord = rd.randrange(size_factor)
            j_coord = rd.randrange(size_factor)
            visited.append([i_coord, j_coord])
            visited_from.append(NULL_DIRECTION)

        else:
            if [i_coord, j_coord] in visited:
                visited.clear()
                visited_from.clear()

            visited.append([i_coord, j_coord])
            can_go = [i_coord > min_coord, j_coord < max_coord, i_coord < max_coord, j_coord > min_coord]
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

    start_i_coord = 2 * rd.randrange(size_factor) + 1
    star_j_coord = min_coord
    finish_i_coord = 2 * rd.randrange(size_factor) + 1
    finish_j_coord = 2 * max_coord + 2

    while maze[start_i_coord, star_j_coord + 1] != PATH:
        start_i_coord = 2 * rd.randrange(size_factor) + 1

    while maze[finish_i_coord, finish_j_coord - 1] != PATH:
        finish_i_coord = 2 * rd.randrange(size_factor) + 1

    maze[start_i_coord, star_j_coord] = PATH
    maze[finish_i_coord, finish_j_coord] = PATH

    return maze, 2 * size_factor + 1, (start_i_coord, star_j_coord), (finish_i_coord, finish_j_coord)

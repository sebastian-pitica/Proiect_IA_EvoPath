# /**************************************************************************
#
#  File:        project.py
#  Copyright:   (c) 2023 EvoPath Team
#  Description:
#  Designed by: Sebastian Pitica
#
#  Module-History:
#  Date        Author                Reason
#  24.11.2023  Matei Rares           Basic structure and functions
#  24.11.2023  Sebastian Pitica      Basic structure and Wilson algorithm for maze gen (improved version from https://github.com/antigones/pymazes/blob/main/wilson.py)
#  27.11.2023  Pitica Sebastian      Updated gen_pathway, todos and imports, rename vars
#  27.11.2023  Matei Rares           Updated name variables and gen_adaptable_pathway(), deleted comments
#  27.11.2023  Sebastian Pitica      Added particle swarm optimization algorithm lb and gb, added fitness func, added manhattan distance func, added eliminate duplicate neighbors func
#  28.11.2023  Sebastian Pitica      Added get_values func, added draw_maze func, added draw_smooth_path func, added run_simulation func, added create_simulation_window func, specific future todos and added maze specific constants
#  29.11.2023  Matei Rares           Normalize angles, modify bug in gen_adaptable_pathway()
#  30.11.2023  Matei Rares           Get values from input window and verify them, animate particles as circles with a number inside, function to draw all particles in maze, draw particles sequentially, added stop animation button
#  **************************************************************************/

#########################################################################################################
#########################################################################################################
############################################## Matei ####################################################
#########################################################################################################
#########################################################################################################

import random

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

normalizeAngle = lambda angle: angle % 360


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
                individual[i - (len(last_tried_dir))] = det_angle_based_on(direction)

            elif maze[row][col + 1] == WALL:
                last_tried_dir.append(RIGHT)

        elif direction == LEFT:
            if col - 1 >= 0:
                if maze[row][col - 1] == PATH:
                    col -= 1
                    last_tried_dir = [RIGHT]
                    coming_direction = RIGHT
                    individual[i - (len(last_tried_dir))] = det_angle_based_on(direction)
                elif maze[row][col - 1] == WALL:
                    last_tried_dir.append(LEFT)
            else:
                last_tried_dir.append(LEFT)

        elif direction == UP:
            if maze[row - 1][col] == PATH:
                row -= 1
                last_tried_dir = [DOWN]
                coming_direction = DOWN
                individual[i - (len(last_tried_dir))] = det_angle_based_on(direction)

            elif maze[row - 1][col] == WALL:
                last_tried_dir.append(UP)
        elif direction == DOWN:
            if maze[row + 1][col] == PATH:
                row += 1
                last_tried_dir = [UP]
                coming_direction = UP
                individual[i - (len(last_tried_dir))] = det_angle_based_on(direction)

            elif maze[row + 1][col] == WALL:
                last_tried_dir.append(DOWN)

        coord = (row, col)
        pathway.append(coord)

    return pathway, individual


#########################################################################################################
#########################################################################################################
############################################### Sebastian ###############################################
#########################################################################################################
#########################################################################################################


import numpy as np
import random as rd
import tkinter as tk
from tkinter import ttk

MAZE_START = (None, None)
MAZE_END = (None, None)
MAZE_SIZE = None
maze = list(list())
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


def particle_swarm_optimization_gbest(population: list, generations: int, consts: dict,canvas) -> list:
    print("population: ", str(population)+ "\n" + "generations: ", str(generations) + "\n" + "consts: ", str(consts))
    population_length = len(population)
    nr_genes = len(population[0])

    speeds: list[list] = [gen_individual(len(population[0])) for _ in range(population_length)]
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

            print(" fitness_personal_bests: ", fitness_personal_bests, " fitness_global_best: ", fitness_global_best)
            if fitness_personal_best > fitness_global_best:
                global_best, fitness_global_best = personal_best, fitness_personal_best

            vi = [normalizeAngle(consts['w'] * vi[j] +
                   consts['c1'] * consts['r1'] * (personal_best[j] - xi[j]) +
                   consts['c2'] * consts['r2'] * (global_best[j] - xi[j]))
                  for j in range(0, nr_genes)]
            # (todo) apelare normalizare peste  vi
            #vi = normalizeAngle(vi)
            xi = xi + vi
            xi= [normalizeAngle(ind) for ind in xi]

            # (todo) apelare normalizare peste xi

            ###########################################################################
            population[i] = xi
            speeds[i] = vi
            personal_bests[i] = personal_best
            fitness_personal_bests[i] = fitness_personal_best

            path,_=gen_adaptable_pathway(population[i])
            draw_smooth_path(canvas, path, 30, i)

            # gen pathway for population[i] sau xi
            # cu ce s a generat pornesti animatie cu nr particula i
            # print up side corner genereation nr

    return global_best


def particle_swarm_optimization_lbest(population: list, generations: int, consts: dict) -> list:
    population_length = len(population)
    nr_genes = len(population[0])

    local_bests = [population[0], population[0]]
    fitness_local_bests = list()
    fitness_local_bests[0], local_bests[0] = adaptable_fitness_function(local_bests[0])
    fitness_local_bests[1], local_bests[1] = adaptable_fitness_function(local_bests[1])

    speeds: list[list] = [gen_individual(len(population[0])) for _ in range(population_length)]
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

            if fitness_personal_best > fitness_local_best:
                local_best, fitness_local_best = personal_best, fitness_personal_best

            vi = [(consts['w'] * vi[j] +
                   consts['c1'] * consts['r1'] * (personal_best[j] - xi[j]) +
                   consts['c2'] * consts['r2'] * (local_best[j] - xi[j]))
                  for j in range(0, nr_genes)]
            # (todo) apelare normalizare peste  vi
            vi = normalizeAngle(vi)
            xi = normalizeAngle(xi + vi)

            # (todo) apelare normalizare peste xi

            ###########################################################################
            population[i] = xi
            speeds[i] = vi
            personal_bests[i] = personal_best
            fitness_personal_bests[i] = fitness_personal_best
            local_bests[i % 2] = local_best
            fitness_local_bests[i % 2] = fitness_local_best

            # gen pathway for population[i] sau xi
            # cu ce s a generat pornesti animatie cu nr particula i
            # print up side corner genereation nr
    return local_bests


def particle_swarm_optimization(population_length: int, nr_genes: int, generations: int,
                                consts: dict):
    population = gen_population(nr_genes, population_length)
    gbest = particle_swarm_optimization_gbest(population, generations, consts)

    lbest = particle_swarm_optimization_lbest(population, generations, consts)
    # todo return gbest and lbest
    # (todo) print gbest and lbest on window


def gen_maze_wilson(size_factor: int) -> (np.ndarray, int, tuple, tuple):
    global maze, MAZE_START, MAZE_END
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
    MAZE_START = (start_i_coord, star_j_coord)
    MAZE_END = (finish_i_coord, finish_j_coord)

    return 2 * size_factor + 1


consts = {'w': 0, 'c1': 0, 'r1': 0, 'r2': 0, 'c2': 0}
GENES = 0
INDIVIDUALS = 0
GENERATIONS = 0
ANIMATION_SPEED = 0
input_window = 0


def get_values(entry_w, entry_c1, entry_r1, entry_r2, entry_c2, entry_gene_length, entry_population_length,
               entry_generations, entry_maze_size_factor, animation_speed_factor):
    global consts, GENES, INDIVIDUALS, GENERATIONS, ANIMATION_SPEED, MAZE_SIZE

    consts['w'] = 11 if entry_w == '' else int(entry_w)
    consts['c1'] = 11 if entry_c1 == '' else int(entry_c1)
    consts['r1'] = 11 if entry_r1 == '' else int(entry_r1)
    consts['r2'] = 11 if entry_r2 == '' else int(entry_r2)
    consts['c2'] = 11 if entry_c2 == '' else int(entry_c2)
    GENES = 11 if entry_gene_length == '' else int(entry_gene_length)
    INDIVIDUALS = 11 if entry_population_length == '' else int(entry_population_length)
    GENERATIONS = 11 if entry_generations == '' else int(entry_generations)
    MAZE_SIZE = 11 if entry_maze_size_factor == '' else int(entry_maze_size_factor)
    ANIMATION_SPEED = 11 if animation_speed_factor == '' else int(animation_speed_factor)


def draw_maze(maze, canvas, width, height):
    canvas.delete("all")
    scale_factor = min(width / len(maze[0]), height / len(maze))

    # can be used to center the maze, to move it around or to draw multiple mazes on the same canvas
    x_offset = 0
    y_offset = 0

    for i, row in enumerate(maze):
        for j, char in enumerate(row):
            if char == '#':
                canvas.create_rectangle(j * scale_factor + x_offset, i * scale_factor + y_offset,
                                        (j + 1) * scale_factor + x_offset, (i + 1) * scale_factor + y_offset,
                                        fill='green')


# todo should be called from the simulation window after every particle
# todo in the end the particle should be cleared
def draw_smooth_path(canvas, path_coords, scale_factor, particle_number):
    path_coords.append(path_coords[-1])  # Add the last point again to make the animation smoother
    #path_coords[len(path_coords)] = path_coords[-1]  # Add the last point again to make the animation smoother

    def animate(index):
        if index < len(path_coords) - 1:
            y1, x1 = path_coords[index]
            y2, x2 = path_coords[index + 1]
            # x1,y1 = path_coords[index]
            # x2,y2 = path_coords[index + 1]

            steps = 20 if (x1, y1) != (x2, y2) else 1
            x_step = (x2 - x1) / steps
            y_step = (y2 - y1) / steps
            for step in range(steps):
                x = x1 + step * x_step
                y = y1 + step * y_step

                canvas.delete("smooth_point")

                canvas.create_oval(x * scale_factor, y * scale_factor,
                                   (x + 1) * scale_factor, (y + 1) * scale_factor,
                                   fill="purple", outline="black", tags="smooth_point"
                                   )

                canvas.create_text((x + 0.5) * scale_factor, (y + 0.5) * scale_factor,
                                   text=str(particle_number), fill='white', tags="smooth_point")
                canvas.update()
                canvas.after(1)
            canvas.after(0, animate, index + 1)
        else:
            canvas.delete("smooth_point")

    animate(0)


def draw_all(scale_factor, paths, canvas):
    def update_animation(index):
        for i, path in enumerate(paths):
            if index < len(path) - 1:
                y1, x1 = path[index]
                x = x1
                y = y1

                canvas.delete(f"robot_{i}")
                canvas.create_oval(x * scale_factor, y * scale_factor,
                                   (x + 1) * scale_factor, (y + 1) * scale_factor,
                                   fill="purple", outline="black", tags=f"robot_{i}")

                canvas.create_text((x + 0.5) * scale_factor, (y + 0.5) * scale_factor,
                                   text=str(i), fill='white', tags=f"robot_{i}")
                canvas.update()
                canvas.after(50)

        canvas.after(0, update_animation, index + 1)

    update_animation(0)


def stop_animation():
    print("Setez valoare ca sa iasa din bucla animatiei")


def run_simulation():
    global MAZE_SIZE, maze
    simulation_window = tk.Tk()
    simulation_window.title("Simulation")
    simulation_window.resizable(True, True)
    fixed_canvas_width = 740
    fixed_canvas_height = 740
    offset_x = 400;
    offset_y = 100;
    simulation_window.geometry(f"{fixed_canvas_width}x{fixed_canvas_height}+{offset_x}+{offset_y}")

    canvas = tk.Canvas(simulation_window, width=fixed_canvas_width, height=fixed_canvas_height)
    canvas.pack()
    button = tk.Button(simulation_window, text="Stop Animation!", command=stop_animation)
    button.place(relx=1.0, rely=0.0,
                 anchor='ne')  # relx=0.0 means the left edge, rely=0.0 means the top edge, anchor='nw' means northwest

    ##########################################################################################
    population=[]
    for i in range(INDIVIDUALS):
        population.append(gen_individual(GENES))

    gen_maze_wilson(MAZE_SIZE)

    draw_maze(maze, canvas, len(maze) * 30, len(maze) * 30)

    particle_swarm_optimization_gbest(population, GENERATIONS, consts, canvas)
   # particle_swarm_optimization_lbest(population, GENERATIONS, consts)

    paths = []
    pathway, _ = gen_adaptable_pathway(gen_individual(80))
    paths.append(pathway)
    pathway, _ = gen_adaptable_pathway(gen_individual(80))
    paths.append(pathway)

    draw_all(30, paths, canvas)

    ##########################################################################################

    simulation_window.mainloop()

    # todo take values from input window x
    # todo check them x
    # todo generate maze x
    # todo run simulation from gbest button and from lbest button
    # todo draw particles on maze animations x

    # todo after maze is generated set it to maze variable  -> global maze in wilson ?
    # todo take animation speed from input window x
    # todo add a button to stop the animation x-stop and resume?
    # todo add a button to stop the simulation
    # todo draw particles as circles with a number inside x
    # todo make windows of fixed size x
    # todo fill the input window with default values x-default from window or from validation?
    # todo when run the simulation call the pos function with the specific params
    # todo at the end of the simulation clear the particles from the maze and provide the results
    # albastru maze rosu particle
    # valori din
    # din alg cu gbest setez in dictionaru cu consts[]


def create_simulation_window():
    input_window = tk.Tk()

    fixed_input_window_width = 300
    fixed_input_window_height = 300
    input_window.title("Input values for simulation")
    input_window.resizable(False, False)
    offset_x = 100;
    offset_y = 50;
    input_window.geometry(f"{fixed_input_window_width}x{fixed_input_window_height}+{offset_x}+{offset_y}")

    # Create and place input labels and entry widgets
    tk.Label(input_window, text="w:").grid(row=0, column=0)

    entry_w = tk.Entry(input_window)
    entry_w.grid(row=0, column=1)
    entry_w.insert(0, "11")

    tk.Label(input_window, text="c1:").grid(row=1, column=0)
    entry_c1 = tk.Entry(input_window)
    entry_c1.grid(row=1, column=1)
    entry_c1.insert(1, "11")

    tk.Label(input_window, text="r1:").grid(row=2, column=0)
    entry_r1 = tk.Entry(input_window)
    entry_r1.grid(row=2, column=1)
    entry_r1.insert(2, "11")

    tk.Label(input_window, text="r2:").grid(row=3, column=0)
    entry_r2 = tk.Entry(input_window)
    entry_r2.grid(row=3, column=1)
    entry_r2.insert(3, "11")

    tk.Label(input_window, text="c2:").grid(row=4, column=0)
    entry_c2 = tk.Entry(input_window)
    entry_c2.grid(row=4, column=1)
    entry_c2.insert(4, "11")

    tk.Label(input_window, text="Individual Gene Length:").grid(row=5, column=0)
    entry_gene_length = tk.Entry(input_window)
    entry_gene_length.grid(row=5, column=1)
    entry_gene_length.insert(5, "11")

    tk.Label(input_window, text="Population Length:").grid(row=6, column=0)
    entry_population_length = tk.Entry(input_window)
    entry_population_length.grid(row=6, column=1)
    entry_population_length.insert(6, "11")

    tk.Label(input_window, text="Generations:").grid(row=7, column=0)
    entry_generations = tk.Entry(input_window)
    entry_generations.grid(row=7, column=1)
    entry_generations.insert(7, "11")

    tk.Label(input_window, text="Maze Size Factor:").grid(row=8, column=0)
    entry_maze_size_factor = tk.Entry(input_window)
    entry_maze_size_factor.grid(row=8, column=1)
    entry_maze_size_factor.insert(8, "11")

    tk.Label(input_window, text="Animation speed:").grid(row=9, column=0)
    animation_speed = tk.Entry(input_window)
    animation_speed.grid(row=9, column=1)
    animation_speed.insert(9, "11")

    submit_button = ttk.Button(input_window, text="Run simulation", command=lambda: (
        get_values(entry_w.get(), entry_c1.get(), entry_r1.get(), entry_r2.get(), entry_c2.get(),
                   entry_gene_length.get(),
                   entry_population_length.get(), entry_generations.get(), entry_maze_size_factor.get(),
                   animation_speed.get())
        , run_simulation()))
    submit_button.grid(row=10, column=0, columnspan=2, pady=10)

    input_window.mainloop()


if __name__ == '__main__':
    create_simulation_window()

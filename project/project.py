# /**************************************************************************
#
#  File:        project.py
#  Copyright:   (c) 2023 EvoPath Team
#  Designed by: Sebastian Pitica
#
#  Module-History:
#  Date        Author                Reason
#  24.11.2023  Matei Rares           Basic structure and functions
#  24.11.2023  Sebastian Pitica      Basic structure and Wilson algorithm for maze gen (improved version from https://github.com/antigones/pymazes/blob/main/wilson.py)
#  27.11.2023  Sebastian Pitica     Updated gen_pathway, todos and imports, rename vars
#  27.11.2023  Matei Rares           Updated name variables and gen_adaptable_pathway(), deleted comments
#  27.11.2023  Sebastian Pitica      Added particle swarm optimization algorithm lb and gb, added fitness func, added manhattan distance func, added eliminate duplicate neighbors func
#  28.11.2023  Sebastian Pitica      Added get_values func, added draw_maze func, added draw_smooth_path func, added run_simulation func, added create_simulation_window func, specific future todos and added maze specific constants
#  29.11.2023  Matei Rares           Normalize angles, modify bug in gen_adaptable_pathway()
#  30.11.2023  Matei Rares           Get values from input window and verify them, animate particles as circles with a number inside, function to draw all particles in maze, draw particles sequentially, added stop animation button
#  30.11.2023  Sebastian Pitica      Patched pso functions
#  4.12.2023   Matei Rares           Modified animations
#  9.12.2023   Matei Rares           Option to chose and return gbest or lbest
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

normalize_angle = lambda angle: angle % 360


def gen_rand_angle():
    return random.uniform(0, 360)


def gen_individual(nr_genes):
    individual = []
    for _ in range(nr_genes):
        individual.append(gen_rand_angle())
    return individual


def gen_population(nr_genes, population_length):
    population = []
    for _ in range(population_length):
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
        row, col = coord
        gen = individual[i]
        direction = det_direction(gen)

        if direction in last_tried_dir:
            temp_dir = get_rand_dir_different_from(last_tried_dir)
            if temp_dir != UNBLOCK:
                direction = temp_dir
            else:
                direction = coming_direction

        if direction == RIGHT:
            if col + 1 == MAZE_SIZE:
                col += 1
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
from tkinter import ttk, messagebox

MAZE_START = (None, None)
MAZE_END = (None, None)
MAZE_SIZE = None
maze = list(list())
NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4
NULL_DIRECTION = 0
PATH = '+'
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
            ((1.0 / unique_steps_count) * MAZE_SIZE * 1000 if had_finished else 0)  # Unique steps component
            + (200 * MAZE_SIZE if had_finished else 0)  # Finished maze component extra
            - (remaining_distance * 20)  # Remaining distance component
            - (duplicate_steps_penalty * 10)  # Duplicate steps component
    )
    # The fitness value will be higher for solutions that take fewer unique steps, have less remaining distance,
    # and fewer duplicate steps.

    return fitness_value, individual


def particle_swarm_optimization_gbest(population: list, generations: int, consts: dict, canvas,
                                      generation_label) -> list:
    population_length = len(population)
    nr_genes = len(population[0])
    speeds: list[list] = [gen_individual(len(population[0])) for _ in range(population_length)]
    personal_bests: list[list] = [population[i] for i in range(0, population_length)]
    fitness_personal_bests: list = [0 for _ in range(population_length)]

    global_best: list = population[0]
    fitness_global_best, global_best = adaptable_fitness_function(global_best)

    for generation in range(0, generations):
        for i in range(0, population_length):
            xi: list = population[i]
            vi: list = speeds[i]
            personal_best: list = personal_bests[i]
            fitness_personal_best: int = fitness_personal_bests[i]
            ###########################################################################

            fitness, xi = adaptable_fitness_function(xi)

            if fitness > fitness_personal_best:
                personal_best, fitness_personal_best = xi, fitness

            if fitness_personal_best > fitness_global_best:
                global_best, fitness_global_best = personal_best, fitness_personal_best

            vi = [normalize_angle(consts['w'] * vi[j] +
                                  consts['c1'] * consts['r1'] * (personal_best[j] - xi[j]) +
                                  consts['c2'] * consts['r2'] * (global_best[j] - xi[j]))
                  for j in range(0, nr_genes)]

            xi = xi + vi
            xi = [normalize_angle(ind) for ind in xi]

            ###########################################################################
            population[i] = xi
            speeds[i] = vi
            personal_bests[i] = personal_best
            fitness_personal_bests[i] = fitness_personal_best

        path, _ = gen_adaptable_pathway(global_best)
        draw_smooth_path(canvas, path, DRAW_SIZE_FACTOR, "G")
        draw_generation_nr(canvas, generation_label, generation + 1)
    return global_best


def particle_swarm_optimization_lbest(population: list, generations: int, consts: dict, canvas,
                                      generation_label) -> list:
    population_length = len(population)
    nr_genes = len(population[0])

    local_bests = [population[0], population[0]]
    fitness_local_bests = [[], []]
    fitness_local_bests[0], local_bests[0] = adaptable_fitness_function(local_bests[0])
    fitness_local_bests[1], local_bests[1] = adaptable_fitness_function(local_bests[1])

    speeds: list[list] = [gen_individual(len(population[0])) for _ in range(population_length)]
    personal_bests: list[list] = [population[i] for i in range(0, population_length)]
    fitness_personal_bests: list = [0 for _ in range(population_length)]

    for generation in range(0, generations):
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

            vi = [normalize_angle((consts['w'] * vi[j] +
                                   consts['c1'] * consts['r1'] * (personal_best[j] - xi[j]) +
                                   consts['c2'] * consts['r2'] * (local_best[j] - xi[j])))
                  for j in range(0, nr_genes)]

            xi = xi + vi
            xi = [normalize_angle(ind) for ind in xi]

            ###########################################################################
            population[i] = xi
            speeds[i] = vi
            personal_bests[i] = personal_best
            fitness_personal_bests[i] = fitness_personal_best
            local_bests[i % 2] = local_best
            fitness_local_bests[i % 2] = fitness_local_best
        path, _ = gen_adaptable_pathway(local_best)
        draw_smooth_path(canvas, path, DRAW_SIZE_FACTOR, "L")
        draw_generation_nr(canvas, generation_label, generation + 1)
    return local_bests


GLOBAL = "GLOBAL"
LOCAL = "LOCAL"


def particle_swarm_optimization(population_length: int, nr_genes: int, generations: int,
                                consts: dict, canvas, generation_label):
    population = gen_population(nr_genes, population_length)
    result = None
    if SWITCH_BEST == LOCAL:
        result = particle_swarm_optimization_lbest(population, generations, consts, canvas, generation_label)
    elif SWITCH_BEST == GLOBAL:
        result = particle_swarm_optimization_gbest(population, generations, consts, canvas, generation_label)
    return result


def gen_maze_wilson(size_factor: int) -> (np.ndarray, int, tuple, tuple):
    global maze, MAZE_START, MAZE_END, MAZE_SIZE
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
    MAZE_SIZE = 2 * size_factor + 1


consts = {'w': 0.0, 'c1': 0.0, 'r1': 0.0, 'r2': 0.0, 'c2': 0.0}
GENES = 0
INDIVIDUALS = 0
GENERATIONS = 0
ANIMATION_SPEED = 0
PARTICLE_COLOR = "red"
MAZE_COLOR = "blue"


def get_values_and_start(entry_w, entry_c1, entry_c2, entry_gene_length, entry_population_length,
                         entry_generations, entry_maze_size_factor, animation_speed_factor, global_var, local_var):
    global consts, GENES, INDIVIDUALS, GENERATIONS, ANIMATION_SPEED, SIZE_FACTOR, SWITCH_BEST

    if global_var == True and local_var == True:
        messagebox.showinfo("Information", "Alege un singur best")
        SWITCH_BEST = None
        return
    elif global_var == False and local_var == False:
        messagebox.showinfo("Information", "Alege gbest sau lbest")
        SWITCH_BEST = None
        return
    elif global_var == True and local_var == False:
        SWITCH_BEST = GLOBAL
    elif global_var == False and local_var == True:
        SWITCH_BEST = LOCAL

    consts['w'] = 10 if entry_w == '' else float(entry_w)
    consts['c1'] = 10 if entry_c1 == '' else float(entry_c1)
    consts['c2'] = 10 if entry_c2 == '' else float(entry_c2)
    ####### random(0,1)
    consts['r1'] = random.random()
    consts['r2'] = random.random()
    #######
    GENES = 10 if entry_gene_length == '' else int(entry_gene_length)
    INDIVIDUALS = 10 if entry_population_length == '' else int(entry_population_length)
    GENERATIONS = 10 if entry_generations == '' else int(entry_generations)
    SIZE_FACTOR = 10 if entry_maze_size_factor == '' else int(entry_maze_size_factor)
    ANIMATION_SPEED = 900 if (animation_speed_factor == '' or animation_speed_factor == 1000) else int(
        animation_speed_factor)

    run_simulation()


def draw_maze(maze, canvas, width, height):
    canvas.delete("all")
    scale_factor = min(width / len(maze[0]), height / len(maze))

    x_offset = 0
    y_offset = 0

    for i, row in enumerate(maze):
        for j, char in enumerate(row):
            if char == '#':
                canvas.create_rectangle(j * scale_factor + x_offset, i * scale_factor + y_offset,
                                        (j + 1) * scale_factor + x_offset, (i + 1) * scale_factor + y_offset,
                                        fill=MAZE_COLOR)


def draw_smooth_path(canvas, path_coords, scale_factor, particle_number):
    global ANIMATION_SPEED
    path_coords.append(path_coords[-1])

    def animate(index):
        if index < len(path_coords) - 1:
            y1, x1 = path_coords[index]
            y2, x2 = path_coords[index + 1]

            speed_factor = abs(1000 - ANIMATION_SPEED)
            steps = speed_factor if (x1, y1) != (x2, y2) else 1
            x_step = (x2 - x1) / steps
            y_step = (y2 - y1) / steps
            for step in range(steps):
                x = x1 + step * x_step
                y = y1 + step * y_step

                canvas.delete(f"smooth_point{particle_number}")

                canvas.create_oval(x * scale_factor, y * scale_factor,
                                   (x + 1) * scale_factor, (y + 1) * scale_factor,
                                   fill=PARTICLE_COLOR, outline="black", tags=f"smooth_point{particle_number}"
                                   )

                canvas.create_text((x + 0.5) * scale_factor, (y + 0.5) * scale_factor,
                                   text=str(particle_number), fill='white', tags=f"smooth_point{particle_number}")
                canvas.update()
                # canvas.after(1)
            canvas.after(0, animate, index + 1)
        else:
            canvas.delete(f"smooth_point{particle_number}")

    animate(0)


def draw_all(scale_factor, paths, canvas):
    def update_animation(index):
        for i, pat in enumerate(paths):
            if index <= len(pat) - 1:
                y1, x1 = pat[index]
                x = x1
                y = y1

                canvas.delete(f"robot_{i}")
                canvas.create_oval(x * scale_factor, y * scale_factor,
                                   (x + 1) * scale_factor, (y + 1) * scale_factor,
                                   fill=PARTICLE_COLOR, outline="black", tags=f"robot_{i}")

                canvas.create_text((x + 0.5) * scale_factor, (y + 0.5) * scale_factor,
                                   text=str(i), fill='white', tags=f"robot_{i}")
                canvas.update()
                speed_factor = abs(1000 - ANIMATION_SPEED)

                canvas.after(speed_factor)
            else:
                canvas.delete(f"robot_{i}")
                return

        canvas.after(0, update_animation, index + 1)

    update_animation(0)


DRAW_SIZE_FACTOR = 30
SWITCH_BEST = None
SIZE_FACTOR = 0


def draw_generation_nr(canvas, label, generation_nr):
    label.config(text=f"Generation: {generation_nr}")
    canvas.update()


def run_simulation():
    global maze, SIZE_FACTOR, DRAW_SIZE_FACTOR, MAZE_SIZE, consts

    if SWITCH_BEST is not None:
        simulation_window = tk.Tk()
        simulation_window.title("Simulation")
        simulation_window.resizable(True, True)
        gen_maze_wilson(SIZE_FACTOR)
        fixed_canvas_width = MAZE_SIZE * DRAW_SIZE_FACTOR
        fixed_canvas_height = MAZE_SIZE * DRAW_SIZE_FACTOR

        center_x = int(simulation_window.winfo_screenwidth() / 2)
        center_y = int(simulation_window.winfo_screenheight() / 2)
        offset_x = center_x - int(fixed_canvas_width / 2);
        offset_y = center_y - int(fixed_canvas_height / 2);
        simulation_window.geometry(f"{fixed_canvas_width}x{fixed_canvas_height}+{offset_x}+{offset_y}")

        canvas = tk.Canvas(simulation_window, width=fixed_canvas_width, height=fixed_canvas_height)
        canvas.pack()

        generation_label = tk.Label(simulation_window, text="Generation: ")
        generation_label.place(relx=0.0, rely=0.0, anchor='nw')

        ##########################################################################################

        draw_maze(maze, canvas, MAZE_SIZE * DRAW_SIZE_FACTOR, MAZE_SIZE * DRAW_SIZE_FACTOR)
        best = particle_swarm_optimization(INDIVIDUALS, GENES, GENERATIONS, consts, canvas, generation_label)
        print("Local best: ", best) if SWITCH_BEST == LOCAL else print("Global best: ", best)

        simulation_window.mainloop()


def create_simulation_window():
    input_window = tk.Tk()

    fixed_input_window_width = 300
    fixed_input_window_height = 250
    input_window.title("Input values for simulation")
    input_window.resizable(False, False)
    offset_x = 100
    offset_y = 350

    input_window.geometry(f"{fixed_input_window_width}x{fixed_input_window_height}+{offset_x}+{offset_y}")
    tk.Label(input_window, text="w:").grid(row=0, column=0)

    entry_w = tk.Entry(input_window)
    entry_w.grid(row=0, column=1)
    entry_w.insert(0, "1")

    tk.Label(input_window, text="c1:").grid(row=1, column=0)
    entry_c1 = tk.Entry(input_window)
    entry_c1.grid(row=1, column=1)
    entry_c1.insert(1, "1.5")

    tk.Label(input_window, text="c2:").grid(row=2, column=0)
    entry_c2 = tk.Entry(input_window)
    entry_c2.grid(row=2, column=1)
    entry_c2.insert(2, "2")

    tk.Label(input_window, text="Individual Gene Length:").grid(row=3, column=0)
    entry_gene_length = tk.Entry(input_window)
    entry_gene_length.grid(row=3, column=1)
    entry_gene_length.insert(3, "20")

    tk.Label(input_window, text="Population Length:").grid(row=4, column=0)
    entry_population_length = tk.Entry(input_window)
    entry_population_length.grid(row=4, column=1)
    entry_population_length.insert(4, "10")

    tk.Label(input_window, text="Generations:").grid(row=5, column=0)
    entry_generations = tk.Entry(input_window)
    entry_generations.grid(row=5, column=1)
    entry_generations.insert(5, "10")

    tk.Label(input_window, text="Maze Size Factor:").grid(row=6, column=0)
    entry_maze_size_factor = tk.Entry(input_window)
    entry_maze_size_factor.grid(row=6, column=1)
    entry_maze_size_factor.insert(6, "6")

    tk.Label(input_window, text="Animation speed:").grid(row=7, column=0)
    animation_speed = tk.Entry(input_window)
    animation_speed.grid(row=7, column=1)
    animation_speed.insert(7, "930")

    global_checkbox_var = tk.BooleanVar()
    global_checkbox_var.set(True)
    local_checkbox_var = tk.BooleanVar()
    local_checkbox_var.set(False)

    checkbox1 = tk.Checkbutton(input_window, text="Global best", variable=global_checkbox_var)
    checkbox1.grid(row=8, column=0)

    checkbox2 = tk.Checkbutton(input_window, text="Local best", variable=local_checkbox_var)
    checkbox2.grid(row=8, column=1)

    submit_button = ttk.Button(input_window, text="Run simulation", command=lambda: (
        get_values_and_start(entry_w.get(), entry_c1.get(), entry_c2.get(),
                             entry_gene_length.get(),
                             entry_population_length.get(), entry_generations.get(), entry_maze_size_factor.get(),
                             animation_speed.get(), global_checkbox_var.get(), local_checkbox_var.get())))
    submit_button.grid(row=9, column=0, columnspan=2, pady=10)

    input_window.mainloop()


if __name__ == '__main__':
    create_simulation_window()

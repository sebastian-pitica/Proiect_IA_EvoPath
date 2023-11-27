# /**************************************************************************
#
#  File:        matei.py
#  Copyright:   (c) 2023 EvoPath Team
#  Description:
#  Designed by: Matei Rares
#
#  Module-History:
#  Date        Author                Reason
#  24.11.2023  Matei Rares          Basic structure
#  27.11.2023  Pitica Sebastian     Updated gen_pathway, todos and imports
#
#  **************************************************************************/

import random
from general_use import maze, MAZE_START, MAZE_END, MAZE_SIZE
from seba import PATH, WALL

# todo name the variables from consts to functions vars in english

DREAPTA = "dreapta"
STANGA = "stanga"
SUS = "sus"
JOS = "jos"
DEBLOCARE = "deblocare"
DIRECTII = [DREAPTA, STANGA, SUS, JOS]
LIMITA_SUPERIOARA_UNGHI_DREAPTA = 45
LIMITA_INFERIOARA_UNGHI_DREAPTA = 315
LIMITA_SUPERIOARA_UNGHI_STANGA = 225
LIMITA_INFERIOARA_UNGHI_STANGA = 135
LIMITA_SUPERIOARA_UNGHI_SUS = 135
LIMITA_INFERIOARA_UNGHI_SUS = 45
LIMITA_SUPERIOARA_UNGHI_JOS = 315
LIMITA_INFERIOARA_UNGHI_JOS = 225


def gen_rand_angle():
    return random.uniform(0, 360)


def gen_nr_genes(dim_labirint):
    return random.randint(2 * dim_labirint, dim_labirint * dim_labirint)


def gen_individ(nr_genes):
    individ = []
    for i in range(0, nr_genes):
        individ.append(gen_rand_angle())
    return individ


def gen_population(nr_genes, nr_indivizi):
    population = []
    for i in range(0, nr_indivizi):
        population.append(gen_individ(nr_genes))
    return population


def det_directie(angle):
    if angle > LIMITA_INFERIOARA_UNGHI_DREAPTA or angle < LIMITA_SUPERIOARA_UNGHI_DREAPTA:
        return DREAPTA
    elif LIMITA_INFERIOARA_UNGHI_SUS < angle < LIMITA_SUPERIOARA_UNGHI_SUS:
        return SUS
    elif LIMITA_INFERIOARA_UNGHI_STANGA < angle < LIMITA_SUPERIOARA_UNGHI_STANGA:
        return STANGA
    elif LIMITA_INFERIOARA_UNGHI_JOS < angle < LIMITA_SUPERIOARA_UNGHI_JOS:
        return JOS


# todo remove
# def det_new_coord(curr_coord, gena, dim_labirint):
#     directie = det_directie(gena)
#     """COORDONATELE SUNT REPREZENTATE DE LINII SI COLOANE Y=LINIA, X=COLOANA"""
#     row, col = curr_coord
#     # TODO AICI BLOCAJE
#     if (directie == DREAPTA) and (maze[row][col + 1] == PATH):
#         if col + 1 == dim_labirint:
#             print("S-a ajuns la final")  # se activeaza un flag care copie coordonata pt restu genelor
#         col += 1
#     elif (directie == STANGA) and (col - 1 >= 0) and (maze[row][col - 1] == PATH):
#         # daca pleaca doar din stanga si face stanga nu inainteaza
#         col -= 1
#     elif (directie == SUS) and (maze[row - 1][col] == PATH):
#         row -= 1
#     elif (directie == JOS) and (maze[row + 1][col] == PATH):
#         row += 1
#     return row, col
#


def get_rand_dir_different_from(last_tried_dir):
    lista = [direct for direct in DIRECTII if direct not in last_tried_dir]
    if lista:
        return lista[random.randint(0, len(lista) - 1)]
    else:
        return DEBLOCARE


# todo remove comments
# todo update individual gene if it's blocked and you change the direction
# todo if you find the end, dont copy the end coord till the end of normal pathway len
def gen_adaptable_pathway(individual):
    pathway = []
    walls_coord = []  # variabile contine coordonatele incercate care sunt pereti
    coord = MAZE_START
    pathway.append(coord)

    last_tried_dir = []
    coming_direction = None
    for gen in individual:

        directie = det_directie(gen)
        row, col = coord
        """COORDONATELE SUNT REPREZENTATE DE LINII SI COLOANE Y=LINIA, X=COLOANA"""
        # TODO AICI BLOCAJE
        if directie in last_tried_dir:
            print(last_tried_dir)

            temp_dir = get_rand_dir_different_from(last_tried_dir)
            if temp_dir != DEBLOCARE:
                directie = temp_dir
            else:  # aici s-a blocat de tot deci ii directia din care a venit
                directie = coming_direction

        if directie == DREAPTA:
            if col + 1 == MAZE_SIZE:  # ies din bucla cand ajunge la finish, nr de elem din pathway e distanta
                break
            if maze[row][col + 1] == PATH:
                col += 1
                last_tried_dir = [STANGA]  # pun la incercari directia din care a venit
                coming_direction = STANGA
            elif maze[row][col + 1] == WALL:
                # daca directia nu e in walls, o adaug, daca e dau alta directie
                # if (row, col + 1) in maze:
                #     #new directie
                #     last_tried_dir.append(DREAPTA)
                #     pass
                # else:
                #
                # walls_coord.append((row,
                #                     col + 1))  # daca urm coordonata e WALL o adaug la walls si tin minte directia in care am incercat
                last_tried_dir.append(DREAPTA)

        elif directie == STANGA:
            if col - 1 >= 0:  # daca e la inceput si incearca stanga tine minte
                last_tried_dir.append(STANGA)
            elif maze[row][col - 1] == PATH:
                col -= 1
                last_tried_dir = [DREAPTA]
                coming_direction=DREAPTA
            elif maze[row][col - 1] == WALL:
                walls_coord.append((row, col - 1))
                last_tried_dir.append(STANGA)
        elif directie == SUS:
            if maze[row - 1][col] == PATH:
                row -= 1
                last_tried_dir = [JOS]
                coming_direction=JOS
            elif maze[row - 1][col] == WALL:
                last_tried_dir.append(SUS)
        elif directie == JOS:
            if maze[row + 1][col] == PATH:
                row += 1
                last_tried_dir = [SUS]
                coming_direction=SUS
            elif maze[row + 1][col] == WALL:
                last_tried_dir.append(JOS)

        coord = (row, col)
        pathway.append(coord)

    return pathway, individual


# todo remove
# maze = [["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
#         ["#", " ", " ", " ", "#", " ", "#", " ", " ", " "],
#         ["#", "#", "#", " ", " ", " ", "#", " ", "#", "#"],
#         [" ", " ", "#", "#", " ", "#", "#", " ", "#", "#"],
#         ["#", " ", " ", "#", " ", "#", " ", " ", " ", "#"],
#         ["#", "#", " ", "#", " ", " ", " ", "#", "#", "#"],
#         ["#", " ", " ", "#", " ", "#", "#", "#", " ", "#"],
#         ["#", "#", " ", " ", " ", " ", "#", " ", " ", "#"],
#         ["#", " ", " ", "#", "#", " ", " ", " ", "#", "#"],
#         ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]]
# DIM_LAB = len(maze)
# # mai multe drumuri spre iesire ca sa se minimizeze
# total_population = gen_population(gen_nr_genes(DIM_LAB), 20)
#
# pathways = []
# for ind in total_population:
#     pathways.append(gen_pathway(ind, (3, 0), DIM_LAB))
#
# for path in pathways:
#     print(path)

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
#
#  **************************************************************************/

import random

DREAPTA = "dreapta"
STANGA = "stanga"
SUS = "sus"
JOS = "jos"
NIMIC = " "
CEVA = "+"
#import path wall de la seba care e gol si ocupat

# stringurile: "plus"=perete, "nimic"=nu e nimic(liber)
def gen_rand_angle():
    return random.uniform(0, 360)


def gen_nr_genes(dim_labirint):
    return random.randint(2 * dim_labirint, dim_labirint * dim_labirint)


def det_directie(angle):
    if angle < 45 or angle > 315:
        return "dreapta"  # dreapta
    elif 45 < angle < 135:
        return "sus"  # sus
    elif 135 < angle < 225:
        return "stanga"  # stanga
    elif 225 < angle < 315:
        return "jos"  # jos

#LIMITA_UNGHI_DREAPTA

def det_new_coord(curr_coord, directie, dim_labirint):
    """COORDONATELE SUNT REPREZENTATE DE LINII SI COLOANE Y=LINIA, X=COLOANA"""
    row, col = curr_coord

    if (directie == "dreapta") and (maze[row][col + 1] == " "):
        if col + 1 == dim_labirint:
            print("S-a ajuns la final")
        col += 1
    elif (directie == "stanga") and (col - 1 >= 0) and (
            maze[row][col - 1] == " "):  # daca pleaca doar din stanga si face stanga nu inainteaza
        col -= 1
    elif (directie == "sus") and (maze[row - 1][col] == " "):
        row -= 1
    elif (directie == "jos") and (maze[row + 1][col] == " "):
        row += 1
    return row, col


def gen_individ(nr_genes,start_coord, dim_labirint):
    individ = []
    coord = start_coord
    individ.append(coord)

    for i in range(0, nr_genes):
        directie = det_directie(gen_rand_angle())
        coord = det_new_coord(coord, directie, dim_labirint)
        individ.append(coord)

    return individ


def gen_population(nr_genes,nr_indivizi, start_coord, dim_labirint):
    pop = []
    for i in range(0, nr_indivizi):
        pop.append(gen_individ(nr_genes,start_coord, dim_labirint))
    return pop


maze = [["+", "+", "+", "+", "+", "+", "+", "+", "+", "+"],
        ["+", " ", " ", " ", "+", " ", "+", " ", " ", " "],
        ["+", "+", "+", " ", " ", " ", "+", " ", "+", "+"],
        [" ", " ", "+", "+", " ", "+", "+", " ", "+", "+"],
        ["+", " ", " ", "+", " ", "+", " ", " ", " ", "+"],
        ["+", "+", " ", "+", " ", " ", " ", "+", "+", "+"],
        ["+", " ", " ", "+", " ", "+", "+", "+", " ", "+"],
        ["+", "+", " ", " ", " ", " ", "+", " ", " ", "+"],
        ["+", " ", " ", "+", "+", " ", " ", " ", "+", "+"],
        ["+", "+", "+", "+", "+", "+", "+", "+", "+", "+"]]

popul = gen_population(gen_nr_genes(len(maze)),2, (3, 0), len(maze))
for ind in popul:
    print(ind)

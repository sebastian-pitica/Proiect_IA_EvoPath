import numpy as np
import random as rd


def wilson(grid: np.ndarray, size: int) -> np.ndarray:
    output_grid = np.full([2 * size + 1, 2 * size + 1], '#', dtype=str)
    c = size * size  # number of cells to be visited

    # choose random cell
    i = rd.randrange(size)
    j = rd.randrange(size)
    grid[i, j] = 1

    visited = [[i, j]]
    visited_from = [0]

    while np.count_nonzero(grid) < c:

        if grid[i, j] == 1:
            # already visited, close the loop (carve + empty visited)
            for i in range(len(visited)):
                ve = visited[i]
                vi = ve[0]
                vj = ve[1]
                grid[vi, vj] = 1
                w = 2 * vi + 1
                k = 2 * vj + 1
                output_grid[w, k] = ' '

                vf = visited_from[i]

                if vf == 1:
                    output_grid[w - 1, k] = ' '
                elif vf == 2:
                    output_grid[w, k + 1] = ' '
                elif vf == 3:
                    output_grid[w + 1, k] = ' '
                elif vf == 4:
                    output_grid[w, k - 1] = ' '

            visited.clear()
            visited_from.clear()
            i = rd.randrange(size)
            j = rd.randrange(size)
            visited.append([i, j])
            visited_from.append(0)

        else:
            if [i, j] in visited:
                visited.clear()
                visited_from.clear()

            visited.append([i, j])

            can_go = [1, 1, 1, 1]

            if i == 0:
                can_go[0] = 0
            if i == size - 1:
                can_go[2] = 0
            if j == 0:
                can_go[3] = 0
            if j == size - 1:
                can_go[1] = 0

            neighbour_idx = np.random.choice(np.nonzero(can_go)[0])  # n,e,s,w

            if neighbour_idx == 0:
                visited_from.append(1)
                i -= 1
            elif neighbour_idx == 1:
                visited_from.append(2)
                j += 1
            elif neighbour_idx == 2:
                visited_from.append(3)
                i += 1
            elif neighbour_idx == 3:
                visited_from.append(4)
                j -= 1

    return output_grid


size = 100

np.random.seed(42)
grid = np.zeros(shape=(size, size))

console_grid = wilson(grid, size)


def convert_maze(output_grid):
    maze_list = []
    for row in output_grid:
        maze_row = ['+' if cell == '#' else ' ' for cell in row]
        maze_list.append(maze_row)
    return maze_list


converted_maze = convert_maze(console_grid)

for elm in converted_maze:
    print(str(elm).replace(',', '').replace('[', '').replace(']', '').replace('\'', ''))

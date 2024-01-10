#########################################################################################################
#########################################################################################################
############################################### Sebastian ###############################################
#########################################################################################################
#########################################################################################################

import sys
from unittest import TestCase
import project as project
from unittest.mock import patch, MagicMock

MOCK_ELEMENT = MagicMock()
MOCK_INDIVIDUAL = MOCK_ELEMENT
MOCK_ROUTE_INITIAL = [MOCK_ELEMENT for _ in range(0, 100)]
MOCK_ROUTE_AFTER = [MOCK_ELEMENT for _ in range(0, 50)]
MOCK_ROUTE = MOCK_ROUTE_INITIAL
MAZE_SIZE = 10
FINISHED = True
UNFINISHED = False


class FitnessFunctionTests(TestCase):
    @patch('project.maze_size')
    @patch('project.had_finished')
    @patch('project.gen_adaptable_pathway')
    @patch('project.eliminate_duplicate_neighbors')
    @patch('project.manhattan_distance_to_finish')
    def test_fitness_function_with_finished_route_duplicate_steps(self,
                                                                  mock_manhattan_distance_to_finish,
                                                                  mock_eliminate_duplicate_neighbors,
                                                                  mock_gen_adaptable_pathway,
                                                                  mock_had_finished,
                                                                  mock_maze_size):
        expected_fitness = 1700
        mock_had_finished.return_value = FINISHED
        mock_maze_size.return_value = MAZE_SIZE
        mock_gen_adaptable_pathway.return_value = (MOCK_ROUTE_INITIAL, MOCK_INDIVIDUAL)
        mock_eliminate_duplicate_neighbors.return_value = MOCK_ROUTE_AFTER
        mock_manhattan_distance_to_finish.return_value = 0
        actual_fitness, _ = project.adaptable_fitness_function(MOCK_INDIVIDUAL)
        self.assertEqual(actual_fitness, expected_fitness)

    @patch('project.maze_size')
    @patch('project.had_finished')
    @patch('project.gen_adaptable_pathway')
    @patch('project.eliminate_duplicate_neighbors')
    @patch('project.manhattan_distance_to_finish')
    def test_fitness_function_with_finished_route_unique_steps(self,
                                                               mock_manhattan_distance_to_finish,
                                                               mock_eliminate_duplicate_neighbors,
                                                               mock_gen_adaptable_pathway,
                                                               mock_had_finished,
                                                               mock_maze_size):
        expected_fitness = 2100
        mock_had_finished.return_value = FINISHED
        mock_maze_size.return_value = MAZE_SIZE
        mock_gen_adaptable_pathway.return_value = (MOCK_ROUTE, MOCK_INDIVIDUAL)
        mock_eliminate_duplicate_neighbors.return_value = MOCK_ROUTE
        mock_manhattan_distance_to_finish.return_value = 0
        actual_fitness, _ = project.adaptable_fitness_function(MOCK_INDIVIDUAL)
        self.assertEqual(actual_fitness, expected_fitness)

    @patch('project.maze_size')
    @patch('project.had_finished')
    @patch('project.gen_adaptable_pathway')
    @patch('project.eliminate_duplicate_neighbors')
    @patch('project.manhattan_distance_to_finish')
    def test_fitness_function_with_unfinished_route_duplicate_steps(self,
                                                                    mock_manhattan_distance_to_finish,
                                                                    mock_eliminate_duplicate_neighbors,
                                                                    mock_gen_adaptable_pathway,
                                                                    mock_had_finished,
                                                                    mock_maze_size):
        expected_fitness = -700
        mock_had_finished.return_value = UNFINISHED
        mock_maze_size.return_value = MAZE_SIZE
        mock_gen_adaptable_pathway.return_value = (MOCK_ROUTE_INITIAL, MOCK_INDIVIDUAL)
        mock_eliminate_duplicate_neighbors.return_value = MOCK_ROUTE_AFTER
        mock_manhattan_distance_to_finish.return_value = 10
        actual_fitness, _ = project.adaptable_fitness_function(MOCK_INDIVIDUAL)
        self.assertEqual(actual_fitness, expected_fitness)

    @patch('project.maze_size')
    @patch('project.had_finished')
    @patch('project.gen_adaptable_pathway')
    @patch('project.eliminate_duplicate_neighbors')
    @patch('project.manhattan_distance_to_finish')
    def test_fitness_function_with_unfinished_route_unique_steps(self,
                                                                 mock_manhattan_distance_to_finish,
                                                                 mock_eliminate_duplicate_neighbors,
                                                                 mock_gen_adaptable_pathway,
                                                                 mock_had_finished,
                                                                 mock_maze_size):
        expected_fitness = -200
        mock_had_finished.return_value = UNFINISHED
        mock_maze_size.return_value = MAZE_SIZE
        mock_gen_adaptable_pathway.return_value = (MOCK_ROUTE, MOCK_INDIVIDUAL)
        mock_eliminate_duplicate_neighbors.return_value = MOCK_ROUTE
        mock_manhattan_distance_to_finish.return_value = 10
        actual_fitness, _ = project.adaptable_fitness_function(MOCK_INDIVIDUAL)
        self.assertEqual(actual_fitness, expected_fitness)

    @patch('project.maze_size')
    @patch('project.had_finished')
    @patch('project.gen_adaptable_pathway')
    @patch('project.eliminate_duplicate_neighbors')
    @patch('project.manhattan_distance_to_finish')
    def test_fitness_function_with_unfinished_route_max_remaining_distance(self,
                                                                           mock_manhattan_distance_to_finish,
                                                                           mock_eliminate_duplicate_neighbors,
                                                                           mock_gen_adaptable_pathway,
                                                                           mock_had_finished,
                                                                           mock_maze_size):
        expected_fitness = -184467440737095516140
        mock_had_finished.return_value = UNFINISHED
        mock_maze_size.return_value = MAZE_SIZE
        mock_gen_adaptable_pathway.return_value = (MOCK_ROUTE, MOCK_INDIVIDUAL)
        mock_eliminate_duplicate_neighbors.return_value = MOCK_ROUTE
        mock_manhattan_distance_to_finish.return_value = sys.maxsize
        actual_fitness, _ = project.adaptable_fitness_function(MOCK_INDIVIDUAL)
        self.assertEqual(actual_fitness, expected_fitness)

    @patch('project.maze_size')
    @patch('project.had_finished')
    @patch('project.gen_adaptable_pathway')
    @patch('project.eliminate_duplicate_neighbors')
    @patch('project.manhattan_distance_to_finish')
    def test_fitness_function_with_unfinished_route_min_remaining_distance(self,
                                                                           mock_manhattan_distance_to_finish,
                                                                           mock_eliminate_duplicate_neighbors,
                                                                           mock_gen_adaptable_pathway,
                                                                           mock_had_finished,
                                                                           mock_maze_size):
        expected_fitness = 184467440737095516140
        mock_had_finished.return_value = UNFINISHED
        mock_maze_size.return_value = MAZE_SIZE
        mock_gen_adaptable_pathway.return_value = (MOCK_ROUTE, MOCK_INDIVIDUAL)
        mock_eliminate_duplicate_neighbors.return_value = MOCK_ROUTE
        mock_manhattan_distance_to_finish.return_value = sys.maxsize * -1
        actual_fitness, _ = project.adaptable_fitness_function(MOCK_INDIVIDUAL)
        self.assertEqual(actual_fitness, expected_fitness)


MOCK_CONSTS = {'w': 0.5, 'c1': 0.5, 'r1': 0.5, 'r2': 0.5, 'c2': 0.5}
MOCK_CANVAS = MOCK_ELEMENT
MOCK_GENERATION_LABEL = MOCK_ELEMENT
MOCK_GEN_INDIVIDUAL = [0, 1, 2, 3, 4]
MOCK_BEST_INDIVIDUAL = [13, 1, 99, 16, 45]
MOCK_BEST_INDIVIDUAL_FITNESS = sys.maxsize
MOCK_POPULATION = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]


class TestParticleSwarmOptimizationGBest(TestCase):
    @patch('project.gen_individual')
    @patch('project.adaptable_fitness_function')
    @patch('project.gen_adaptable_pathway')
    @patch('project.draw_smooth_path')
    @patch('project.draw_generation_nr')
    def test_optimization_with_valid_population(self,
                                                mock_draw_generation_nr,
                                                mock_draw_smooth_path,
                                                mock_gen_adaptable_pathway,
                                                mock_adaptable_fitness_function,
                                                mock_gen_individual):
        mock_gen_individual.return_value = MOCK_GEN_INDIVIDUAL
        mock_adaptable_fitness_function.side_effect = [(10, [0, 3, 2, 3, 4]),
                                                       (80, [32, 7, 24, 54, 4]),
                                                       (30, [21, 1, 8, 39, 24]),
                                                       (MOCK_BEST_INDIVIDUAL_FITNESS, MOCK_BEST_INDIVIDUAL),
                                                       (15, [5, 2, 10, 8, 3]),
                                                       (25, [18, 9, 14, 7, 1]),
                                                       (45, [28, 3, 12, 19, 23]),
                                                       (12, [9, 1, 0, 2, 0]),
                                                       (65, [40, 15, 8, 30, 12]),
                                                       (20, [12, 6, 2, 5, 5]),
                                                       (35, [22, 5, 18, 8, 7]),
                                                       (22, [14, 3, 10, 2, 3]),
                                                       (35, [22, 5, 18, 8, 7]),
                                                       (22, [14, 3, 10, 2, 3]),
                                                       (55, [35, 12, 28, 8, 7]),
                                                       (40, [25, 10, 18, 5, 22]),
                                                       (28, [20, 4, 15, 6, 3]),
                                                       (75, [45, 20, 30, 18, 8]),
                                                       (18, [11, 5, 1, 6, 2]),
                                                       (42, [27, 8, 16, 7, 4]),
                                                       (60, [38, 18, 25, 12, 7])]
        mock_gen_adaptable_pathway.return_value = (MOCK_ROUTE, MOCK_INDIVIDUAL)
        generations = 10
        expected_result = MOCK_BEST_INDIVIDUAL
        actual_result = project.particle_swarm_optimization_gbest(MOCK_POPULATION, generations, MOCK_CONSTS,
                                                                  MOCK_CANVAS,
                                                                  MOCK_GENERATION_LABEL)
        self.assertEqual(actual_result, expected_result)

    @patch('project.gen_individual')
    @patch('project.adaptable_fitness_function')
    @patch('project.gen_adaptable_pathway')
    @patch('project.draw_smooth_path')
    @patch('project.draw_generation_nr')
    def test_optimization_with_empty_population(self,
                                                mock_draw_generation_nr,
                                                mock_draw_smooth_path,
                                                mock_gen_adaptable_pathway,
                                                mock_adaptable_fitness_function,
                                                mock_gen_individual):
        mock_gen_individual.return_value = []
        mock_adaptable_fitness_function.return_value = (0, [])
        mock_gen_adaptable_pathway.return_value = ([], [])
        population = []
        generations = 2
        result = project.particle_swarm_optimization_gbest(population, generations, MOCK_CONSTS, MOCK_CANVAS,
                                                           MOCK_GENERATION_LABEL)
        mock_draw_smooth_path.assert_not_called()
        mock_draw_generation_nr.assert_not_called()
        self.assertEqual(result, [])

    @patch('project.gen_individual')
    @patch('project.adaptable_fitness_function')
    @patch('project.gen_adaptable_pathway')
    @patch('project.draw_smooth_path')
    @patch('project.draw_generation_nr')
    def test_optimization_with_zero_generations(self, mock_draw_generation_nr,
                                                mock_draw_smooth_path,
                                                mock_gen_adaptable_pathway,
                                                mock_adaptable_fitness_function,
                                                mock_gen_individual):
        mock_gen_individual.return_value = MOCK_GEN_INDIVIDUAL
        mock_adaptable_fitness_function.return_value = (10, [0, 1, 2, 3, 4])
        mock_gen_adaptable_pathway.return_value = ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
        generations = 0
        result = project.particle_swarm_optimization_gbest(MOCK_POPULATION, generations, MOCK_CONSTS, MOCK_CANVAS,
                                                           MOCK_GENERATION_LABEL)
        mock_draw_generation_nr.assert_not_called()
        mock_draw_smooth_path.assert_not_called()
        self.assertEqual(result, [0, 1, 2, 3, 4])


class TestParticleSwarmOptimizationLBest(TestCase):
    @patch('project.gen_individual')
    @patch('project.adaptable_fitness_function')
    @patch('project.gen_adaptable_pathway')
    @patch('project.draw_smooth_path')
    @patch('project.draw_generation_nr')
    def test_optimization_with_valid_population(self,
                                                mock_draw_generation_nr,
                                                mock_draw_smooth_path,
                                                mock_gen_adaptable_pathway,
                                                mock_adaptable_fitness_function,
                                                mock_gen_individual):
        mock_gen_individual.return_value = MOCK_GEN_INDIVIDUAL
        mock_adaptable_fitness_function.side_effect = [(10, [0, 3, 2, 3, 4]),
                                                       (80, [32, 7, 24, 54, 4]),
                                                       (30, [21, 1, 8, 39, 24]),
                                                       (MOCK_BEST_INDIVIDUAL_FITNESS, MOCK_BEST_INDIVIDUAL),
                                                       (MOCK_BEST_INDIVIDUAL_FITNESS, MOCK_BEST_INDIVIDUAL),
                                                       (15, [5, 2, 10, 8, 3]),
                                                       (50, [15, 25, 6, 4, 0]),
                                                       (25, [18, 9, 14, 7, 1]),
                                                       (55, [35, 12, 28, 8, 7]),
                                                       (40, [25, 10, 18, 5, 22]),
                                                       (28, [20, 4, 15, 6, 3]),
                                                       (60, [38, 18, 25, 12, 7])]
        mock_gen_adaptable_pathway.return_value = (MOCK_ROUTE, MOCK_INDIVIDUAL)
        generations = 5
        expected_result = [MOCK_BEST_INDIVIDUAL, MOCK_BEST_INDIVIDUAL]
        actual_result = project.particle_swarm_optimization_lbest(MOCK_POPULATION, generations, MOCK_CONSTS,
                                                                  MOCK_CANVAS,
                                                                  MOCK_GENERATION_LABEL)
        self.assertEqual(actual_result, expected_result)

    @patch('project.gen_individual')
    @patch('project.adaptable_fitness_function')
    @patch('project.gen_adaptable_pathway')
    @patch('project.draw_smooth_path')
    @patch('project.draw_generation_nr')
    def test_optimization_with_empty_population(self,
                                                mock_draw_generation_nr,
                                                mock_draw_smooth_path,
                                                mock_gen_adaptable_pathway,
                                                mock_adaptable_fitness_function,
                                                mock_gen_individual):
        mock_gen_individual.return_value = []
        mock_adaptable_fitness_function.return_value = (0, [])
        mock_gen_adaptable_pathway.return_value = ([], [])
        population = []
        expected_result = [[], []]
        generations = 2
        actual_result = project.particle_swarm_optimization_lbest(population, generations, MOCK_CONSTS, MOCK_CANVAS,
                                                                  MOCK_GENERATION_LABEL)
        mock_draw_smooth_path.assert_not_called()
        mock_draw_generation_nr.assert_not_called()
        self.assertEqual(actual_result, expected_result)

    @patch('project.gen_individual')
    @patch('project.adaptable_fitness_function')
    @patch('project.gen_adaptable_pathway')
    @patch('project.draw_smooth_path')
    @patch('project.draw_generation_nr')
    def test_optimization_with_zero_generations(self, mock_draw_generation_nr,
                                                mock_draw_smooth_path,
                                                mock_gen_adaptable_pathway,
                                                mock_adaptable_fitness_function,
                                                mock_gen_individual):
        mock_gen_individual.return_value = MOCK_GEN_INDIVIDUAL
        mock_adaptable_fitness_function.return_value = (10, [0, 1, 2, 3, 4])
        mock_gen_adaptable_pathway.return_value = ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])
        generations = 0
        expected_result = [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4]]
        actual_result = project.particle_swarm_optimization_lbest(MOCK_POPULATION, generations, MOCK_CONSTS,
                                                                  MOCK_CANVAS,
                                                                  MOCK_GENERATION_LABEL)
        mock_draw_generation_nr.assert_not_called()
        mock_draw_smooth_path.assert_not_called()
        self.assertEqual(actual_result, expected_result)


class ManhattanDistanceToFinishTests(TestCase):
    @patch('project.maze_end')
    def test_fitness_function_with_finished_route_duplicate_steps(self,
                                                                  mock_maze_end):
        start = (5, 5)
        expected_distance = 0
        mock_maze_end.return_value = (5, 5)
        actual_distance = project.manhattan_distance_to_finish(start)
        self.assertEqual(expected_distance, actual_distance)

    @patch('project.maze_end')
    def test_distance_from_adjacent_point(self,
                                          mock_maze_end):
        start = (5, 4)
        expected_distance = 1
        mock_maze_end.return_value = (5, 5)
        actual_distance = project.manhattan_distance_to_finish(start)
        self.assertEqual(expected_distance, actual_distance)

    @patch('project.maze_end')
    def test_distance_from_diagonal_point(self,
                                          mock_maze_end):
        start = (4, 4)
        expected_distance = 2
        mock_maze_end.return_value = (5, 5)
        actual_distance = project.manhattan_distance_to_finish(start)
        self.assertEqual(expected_distance, actual_distance)

    @patch('project.maze_end')
    def test_distance_from_far_point(self,
                                     mock_maze_end):
        start = (0, 0)
        expected_distance = 10
        mock_maze_end.return_value = (5, 5)
        actual_distance = project.manhattan_distance_to_finish(start)
        self.assertEqual(expected_distance, actual_distance)

    @patch('project.maze_end')
    def test_distance_with_negative_coordinates(self,
                                                mock_maze_end):
        start = (-5, -5)
        expected_distance = 20
        mock_maze_end.return_value = (5, 5)
        actual_distance = project.manhattan_distance_to_finish(start)
        self.assertEqual(expected_distance, actual_distance)


class EliminateDuplicateNeighborsTests(TestCase):

    def test_duplicates_in_consecutive_order(self):
        input_list = [(1, 1), (1, 1), (2, 2), (3, 3), (3, 3), (3, 3)]
        expected_output = [(1, 1), (2, 2), (3, 3)]
        self.assertEqual(project.eliminate_duplicate_neighbors(input_list), expected_output)

    def test_duplicates_not_in_consecutive_order(self):
        input_list = [(1, 1), (2, 2), (1, 1), (3, 3), (2, 2), (3, 3)]
        expected_output = [(1, 1), (2, 2), (1, 1), (3, 3), (2, 2), (3, 3)]
        self.assertEqual(project.eliminate_duplicate_neighbors(input_list), expected_output)

    def test_no_duplicates(self):
        input_list = [(1, 1), (2, 2), (3, 3)]
        expected_output = [(1, 1), (2, 2), (3, 3)]
        self.assertEqual(project.eliminate_duplicate_neighbors(input_list), expected_output)

    def test_empty_input_list(self):
        input_list = []
        expected_output = []
        self.assertEqual(project.eliminate_duplicate_neighbors(input_list), expected_output)


#########################################################################################################
#########################################################################################################
############################################## Matei ####################################################
#########################################################################################################
#########################################################################################################


class TestAdaptablePathway(TestCase):

    # verific daca valorile genelor sunt intre 0 si 360 si daca are nr de gene corecte
    def test_gen_individual(self):
        nr_genes = 20
        ind = project.gen_individual(nr_genes)
        result = True
        i = 0
        for i in range(len(ind)):
            if ind[i] < 0 and ind[i] > 360:
                result = False
        if i != nr_genes - 1:
            result = False

        self.assertEqual(result, True)

    # verific daca populatia are nr de indivizi corect si daca fiecare individ are nr de gene corect
    def test_gen_population(self):
        nr_genes = 20
        nr_indiv = 10
        pop = project.gen_population(nr_genes, nr_indiv)
        result = True
        i = 0
        for i in range(len(pop)):
            if len(pop[i]) != nr_genes:
                result = False
        if i != nr_indiv - 1:
            result = False
        self.assertEqual(result, True)

    # verific daca directia e determinata corect
    def test_det_direction(self):
        ind = [5, 93, 170, 250]
        result = []
        for i in range(len(ind)):
            result.append(project.det_direction(ind[i]))
        self.assertEqual(result, ["right", "up", "left", "down"])

    # verific daca unhgiurile generate se incadreaza in in intervalele corecte
    def test_det_angle_based_on_direction(self):
        ind = ["right", "up", "left", "down"]
        list = []
        result = True
        for i in range(len(ind)):
            list.append(project.det_angle_based_on(ind[i]))
        if (list[0] > 0 and list[0] < 45 or list[0] > 315 and list[0] < 360) != True:
            result = False
        if list[1] < 45 or list[1] > 135:
            result = False
        if list[2] < 135 or list[2] > 225:
            result = False
        if list[3] < 225 or list[3] > 315:
            result = False
        self.assertEqual(result, True)

    # verific daca nr de elemente din path e corect, daca coordonatele sunt mai mari decat -1, mai mici decat marimea maze-ului, si daca coordonatele din path indica zone fara perete
    def test_adaptable_pathway(self):
        result = True
        project.gen_maze_wilson(23)
        nr_genes = 20;
        ind = project.gen_individual(nr_genes)
        path, _ = project.gen_adaptable_pathway(ind)

        if len(path) != nr_genes + 1:
            result = False
        for i in path:
            x, y = i
            if x > project.MAZE_SIZE or y > project.MAZE_SIZE or x < 0 or y < 0 or project.maze[x][y] == project.WALL:
                result = False

        self.assertEqual(result, True)


import unittest

if __name__ == '__main__':
    unittest.main()

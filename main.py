from random import randint

from eckity.algorithms.simple_evolution import SimpleEvolution
from eckity.breeders.simple_breeder import SimpleBreeder
from eckity.creators.ga_creators.bit_string_vector_creator import GABitStringVectorCreator
from eckity.genetic_operators.crossovers.vector_k_point_crossover import VectorKPointsCrossover
from eckity.genetic_operators.mutations.vector_random_mutation import BitStringVectorFlipMutation
from eckity.genetic_operators.selections.tournament_selection import TournamentSelection
from eckity.statistics.best_average_worst_statistics import BestAverageWorstStatistics
from eckity.subpopulation import Subpopulation

from find_meal_evaluator import FindMealEvaluator
import json

def main():
    """
    In the perfect meal problem, there is a pool of food items,
    each having its own weight of fat, carbs and protein and number of calories.
    The goal is to collect the items with the most weight of each category,
    with respect to the percentage of it's importance,
     while not exceeding the maximum calories defined.
    We solve this problem using GA bit vectors, in which the i-th cell is 1 if the i-th item is in the bag, else 0.

    References
    ----------
    DEAP Knapsack Example: https://deap.readthedocs.io/en/master/examples/ga_knapsack.html
    """

    with  open("excelReader.json", "r") as json_file:
        items_dict = json.load(json_file)
        num_items = len(items_dict)
    # Initialize the evolutionary algorithm
    algo = SimpleEvolution(
        Subpopulation(creators=GABitStringVectorCreator(length=1028, gene_creator=GenCreator),
                      population_size=70,
                      # user-defined fitness evaluation method
                      evaluator=FindMealEvaluator(items=items_dict),
                      # maximization problem (fitness is sum of percentage of fat, carbs and protein),
                      # so higher fitness is better
                      higher_is_better=True,
                      elitism_rate=0.0,
                      # genetic operators sequence to be applied in each generation
                      # TODO: test
                      operators_sequence=[
                          VectorKPointsCrossover(probability=0.5, k=2),
                          BitStringVectorFlipMutation(probability=0.05)
                      ],
                      # TODO: test
                      selection_methods=[
                          # (selection method, selection probability) tuple
                          (TournamentSelection(tournament_size=4, higher_is_better=True), 1)
                      ]),
        # TODO: test
        breeder=SimpleBreeder(),
        max_workers=1,
        max_generation=500,
        statistics=BestAverageWorstStatistics()
    )

    # evolve the generated initial population
    algo.evolve()

    # Execute (show) the best solution
    result_list = algo.execute()
    print(result_list)

    def is_one(item: int):
        return item == 1

    # chosen_items = filter(is_one, ())
    print("THe best meal for you contains the following items:\n")
    j = 0
    i = 0
    for item in result_list:
        if type(item) is int and is_one(item):
            item_name = (items_dict[j])["Food name"]
            item_code = (items_dict[j])["Code"]
            print("item number {} ({}) (Code: {}): {}\n".format(i, j, item_code, item_name))
            i += 1
        j += 1


def GenCreator(x, y):
    generator_int = randint(1, 1600)
    if generator_int % 1600 != 0:
        return 0
    return 1


if __name__ == '__main__':
    main()

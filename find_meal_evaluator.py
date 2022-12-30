import random
import numpy as np
import json

from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator

NUM_ITEMS = 500


class FindMealEvaluator(SimpleIndividualEvaluator):
    """
    Evaluator class for finding the perfect meal problem,
    responsible of defining a fitness evaluation method and evaluating it.
    In this example, fitness is the total weight of the categories: fat, carbs, protein, under max_calories calories.
    Attributes
    -------
    items: dict(int, tuple(int, int, int, int))
        dictionary of (item id: (fat, carbs, protein, calories)) of the items
    """

    def __init__(self, items=None, max_calories = 300):
        super().__init__()

        if items is None:
            # Generate random items for the problem
            # TODO: get items from data base or something
            items = {i: (random.randint(1, 300),
                         random.randint(1, 300),
                         random.randint(1, 300),
                         random.randint(1, 150)) for i in range(NUM_ITEMS)}

            """
             - Open the JSON file -
            with open("data.json", "r") as f:
                # Use the json.load() function to read the contents of the file and create a dictionary object
                items = json.load(f)
             - Now you can access the data in the dictionary as you would any other dictionary in Python -
            """

            # TODO: get from user? wanted percentage of fat, carbs and protein of the meal.
            fat = random.randint(1, 100) / 100
            carbs = random.randint(1, 100 - (100 * fat)) / 100
            protein = (100 - (100 * fat) - (100 * carbs)) / 100
        elif type(items) == list:

            for item in items:
                if type(item) is not tuple or type(item[0]) is not int \
                        or type(item[1]) is not int or type(item[2]) is not int or type(item[3]) is not int:
                    raise ValueError('Elements in items list must be tuples of (fat, carbs, protein, calories: int)')

            # Convert items list to dictionary by adding item id
            items = {i: items[i] for i in range(len(items))}
        self.items = items
        self.max_calories = max_calories

    def _evaluate_individual(self, individual):
        """
        Compute the fitness value of a given individual.
        Parameters
        ----------
        individual: Vector
            The individual to compute the fitness value for.
        Returns
        -------
        float
            The evaluated fitness value of the given individual.
        """
        weight, calories = 0, 0
        for i in range(individual.size()):
            if individual.cell_calories(i):
                weight += ((self.items[i][0] * self.fat) + (self.items[i][1] * self.carbs) + (self.items[i][2] * self.protein))
                calories += self.items[i][3]

        # worse possible fitness is returned if the calories of the meal exceeds the maximum calories for a perfect meal
        if calories > self.max_calories:
            return -np.inf

        # fitness value is the total weight (in grams) of the meal
        return weight

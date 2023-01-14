import random
import numpy as np
import json

from eckity.evaluators.simple_individual_evaluator import SimpleIndividualEvaluator
from pandas.io.formats import string



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

    def __init__(self, items=None, max_calories = 1500):
        super().__init__()
        # TODO: get from user? wanted percentage of fat, carbs and protein of the meal.
        self.fat = float(input("What is the percentage of fat you would like to calculate?"))
        self.carbs = float(input("What is the percentage of carbs you would like to calculate?"))
        self.protein = (100 - (100 * self.fat) - (100 * self.carbs)) / 100

        if items is None:
            # Generate random items for the problem
            items = {{"Code": i,
                      "Food name": ''.json(random.choices(string.ascii_letters + string.digits, k = 10)),
                     "Energy": random.uniform(0, 500),
                     "Protein": random.uniform(0, 500),
                     "Carbs": random.uniform(0, 500),
                     "Fat": random.uniform(0, 500)} for i in range(200)}

        elif type(items) == list:

            j = 0
            for item in items:
                # if type(item["Food name"] is not str) \
                #         or (not (item["Energy"]).replace('.', '', 1).isdigit()) \
                #         or (not (item["Protein"]).replace('.', '', 1).isdigit()) \
                #         or (not (item["Carbs"]).replace('.', '', 1).isdigit()) \
                #         or (not (item["Fat"]).replace('.', '', 1).isdigit()) :
                #     raise ValueError('Elements in items list must be dictionary of (name: staring, calories, protein, carbs, fat, : int or floate)')
                # 'in item: Code: {}, Food name: {}, Energy: {}, Protein: {},  Carbs: {}, Fat: {}'.format(
                #                         item["Code"], item["Food name"], item["Energy"], item["Protein"], item["Carbs"], item["Fat"])

                # Convert str to float:
                item["Energy"] = float(item["Energy"])
                item["Protein"] = float(item["Protein"])
                item["Carbs"] = float(item["Carbs"])
                item["Fat"] = float(item["Fat"])
                j += 1

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
            # individual.set_cell_value(i, individual.cell_value(i)*random.randint(0, 1))
            if individual.cell_value(i):
                weight += ((self.items[i]["Fat"] * self.fat) + (self.items[i]["Carbs"] * self.carbs) + (self.items[i]["Protein"] * self.protein))
                calories += self.items[i]["Energy"]

        # worse possible fitness is returned if the calories of the meal exceeds the maximum calories for a perfect meal
        if calories > self.max_calories:
            return -np.inf

        # fitness value is the total weight (in grams) of the meal
        return weight

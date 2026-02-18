"""
Name generation logic.
"""

import random
from utils import decade_from_year, weighted_choice


class NameGenerator:
    """Generates first and last names."""

    def __init__(self, data_loader):
        self.data = data_loader

    def generate_gender(self, year):
        decade = decade_from_year(year)
        prob = self.data.gender_probability[decade]
        return weighted_choice(
            ["male", "female"],
            [prob["male"], prob["female"]],
        )

    def generate_first_name(self, year, gender):
        decade = decade_from_year(year)
        names = self.data.first_names[(decade, gender)]

        choices = [n for n, _ in names]
        weights = [w for _, w in names]

        return weighted_choice(choices, weights)

    def generate_last_name(self):
        return weighted_choice(
            self.data.last_names,
            self.data.last_name_probability,
        )
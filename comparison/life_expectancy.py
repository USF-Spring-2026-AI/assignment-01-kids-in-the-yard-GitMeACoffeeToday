"""
Life expectancy calculations.
"""

import random


class LifeExpectancy:
    """Computes year of death."""

    def __init__(self, data_loader):
        self.data = data_loader

    def calculate_death_year(self, birth_year):
        closest_year = min(
            self.data.life_expectancy,
            key=lambda y: abs(y - birth_year),
        )

        expectancy = self.data.life_expectancy[closest_year]

        variation = random.randint(-10, 10)

        return int(birth_year + expectancy + variation)
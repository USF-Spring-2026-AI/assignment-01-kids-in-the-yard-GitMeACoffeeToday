import random as random
import pandas as pd
import math as math

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from person import Person


class DataFrameHandler:

    def __init__(self, first_names: str,
                 last_names: str,
                 life_expectancy: str,
                 birth_and_marriage_rates: str,
                 gender_name_probability: str,
                 rank_to_probability: str):

        self.first_names = pd.read_csv(f'{first_names}.csv')
        self.last_names = pd.read_csv(f'{last_names}.csv')
        self.life_expectancy = pd.read_csv(f'{life_expectancy}.csv')
        self.birth_and_marriage_rates = pd.read_csv(f'{birth_and_marriage_rates}.csv')
        self.gender_name_probability = pd.read_csv(f'{gender_name_probability}.csv')
        self.rank_to_probability = pd.read_csv(f'{rank_to_probability}.csv')

    @staticmethod
    def normalize_weights(weights: list[float]) -> None:
        """Normalizes the weights of a given list of flaots such that they add up to 1."""
        total_weight = sum(weights)
        if total_weight == 0:
            raise ValueError("List must not be empty and contents must sum to non-zero value")
        for i in range(len(weights)):
            weights[i] = weights[i] / total_weight

    @staticmethod
    def normalize_to_decade(person: Person, int_mode: int = 0) -> int | str:
        """Normalizes and returns a Person's birth year to the relevant decade.
        Returns decade as an int by default, and when int_mode = 1, returns the decade as string. Helper function. """
        if int_mode == 1:
            return math.floor(person.year_born / 10) * 10
        else:
            return f'{math.floor(person.year_born / 10) * 10}s'

    def get_gender(self, era: str):
        """Generates and returns a random gender based on a given era. Helper function."""
        genders = self.gender_name_probability.loc[self.gender_name_probability['decade'] == era, 'gender'].tolist()
        gender_weights = self.gender_name_probability.loc[
            self.gender_name_probability['decade'] == era, 'probability'].tolist()
        name_gender = random.choices(genders, weights=gender_weights, k=1)
        return name_gender[0]

    def gen_random_firstname(self, era: str) -> str:
        """Generates and returns a random first name based on a given era."""
        gender = self.get_gender(era)

        first_names = [str(x) for x in self.first_names.loc[
            (self.first_names['decade'] == era) & (self.first_names['gender'] == gender), 'name']]

        # static type checker freaks out because it doesn't know what's in the created list when we pass it to normalize weights or to choose.
        first_names_weights = [float(x) for x in
                               self.first_names.loc[(self.first_names['decade'] == era) &
                                                    (self.first_names['gender'] == gender), 'frequency']]
        # Make it so the weights all add up to 1
        self.normalize_weights(first_names_weights)
        return random.choices(first_names, weights=first_names_weights, k=1)[0]

    def gen_random_lastname(self, era: str) -> str:
        """Generates and returns a random last name based on a given era."""
        last_names = [str(x) for x in self.last_names.loc[self.last_names['Decade'] == era, 'LastName']]
        probabilities = [float(x) for x in self.rank_to_probability.columns.tolist()]
        self.normalize_weights(probabilities)
        return random.choices(last_names, weights=probabilities, k=1)[0]

    @staticmethod
    def gen_child_lastname(parent: Person) -> str:
        """Self explanatory, returns the last name for a given person."""
        return parent.last_name

    def has_marriage(self, person: Person) -> bool:
        """Decides whether a person, based on their birth year, gets married, returns true or false."""
        marriage_probability = float(self.birth_and_marriage_rates.loc[
                                         self.birth_and_marriage_rates['decade'] == self.normalize_to_decade(
                                             person), 'marriage_rate'].tolist()[0])
        #has_marriage = random.randrange(100) < (marriage_probability*100)

        if marriage_probability:
            return True
        else:
            return False

    def gen_num_children(self, person: Person) -> int:
        """Given a person or couple, based on the eldest of the two -or one-, a random int variable of children is returned."""
        # important note, we always go with the eldest of the couple for consistency
        birth_rate = float(self.birth_and_marriage_rates.loc[
                               self.birth_and_marriage_rates['decade'] == self.normalize_to_decade(
                                   person), 'birth_rate'].iloc[0])

        return random.randrange(int(round(birth_rate - 1.5, 0)), int(round(birth_rate + 1.5, 0)))

    @staticmethod
    def gen_age_range(person: Person) -> tuple[int, int]:
        """Helper function, generates the age range based on a person or their spouse's birth year. Favors the eldest."""
        eldest_age = person.year_born
        if person.spouse is not None:
            if person.spouse.year_born > eldest_age:
                eldest_age = person.spouse.year_born

        return eldest_age + 25, eldest_age + 45

    def gen_year_died(self, person: Person) -> int:
        """Randomly generates year_died for a Person, based on their birth_year"""
        life_expectancy = round(self.life_expectancy.loc[self.life_expectancy[
                                                             'Year'] == person.year_born, 'Period life expectancy at birth'].tolist()[
                                    0], 0)
        plus_minus10 = random.randint(1, 2)
        if plus_minus10 == 1:
            life_expectancy += 10
        elif plus_minus10 == 2:
            life_expectancy -= 10

        return int(life_expectancy + person.year_born)

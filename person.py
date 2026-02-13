import random as random
import numpy as np
from data_frame_handler import DataFrameHandler

class Person:
    def __init__(self):
        self.first_name:str = "" # randomly generated
        self.last_name:str = "" # either randomly generated or passed down from the male parent

        self.parent:Person|None = None
        self.spouse:Person|None = None

        self.children:list[Person] = []

        self.year_born:int = -1
        self.year_died:int = -1

    # for the couple starting off in 1950, bride or your money back
    def progenitor(self, dfh: DataFrameHandler):
        self.year_born = 1950
        self.year_died = dfh.gen_year_died(self)

        self.first_name = dfh.gen_random_firstname(dfh.normalize_to_decade(self))
        self.last_name = dfh.gen_random_lastname(dfh.normalize_to_decade(self))

        self.gen_marriage(dfh, 1)


    def gen_marriage(self, dfh: DataFrameHandler, override:int = 0):
        if dfh.has_marriage(self) or override == 1: # override is to allow progenitor to get a spouse
            new_spouse = Person()
            if self.year_born >= 1960:
                new_spouse.year_born = random.randrange(-10,
                                                        11) + self.year_born  # within 10 years of the original person birth
            else:
                new_spouse.year_born = random.randrange(0,
                                                        10) + self.year_born  # within 10 years of the original person birth

            new_spouse.year_died = dfh.gen_year_died(new_spouse)

            new_spouse.first_name = dfh.gen_random_firstname(dfh.normalize_to_decade(new_spouse))
            new_spouse.last_name = dfh.gen_random_lastname(dfh.normalize_to_decade(new_spouse))

            self.spouse = new_spouse
            new_spouse.spouse = self


    def gen_children(self, dfh: DataFrameHandler) -> tuple[Person, ...]:
        num_children = dfh.gen_num_children(self)
        age_range_df = dfh.gen_age_range(self)

        child_birth_ages = [int(x) for x in np.linspace(age_range_df[0], age_range_df[1], num_children)]
        child_list: list[Person] = []

        for x in range(len(child_birth_ages)):
            new_person = Person()

            new_person.year_born = child_birth_ages[x]
            new_person.year_died = dfh.gen_year_died(new_person)

            new_person.first_name = dfh.gen_random_firstname(dfh.normalize_to_decade(self))
            new_person.last_name = dfh.gen_random_lastname(dfh.normalize_to_decade(self))

            new_person.parent = self

            child_list.append(new_person)

        return tuple(child_list)



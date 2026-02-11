import random as random
import pandas as pd
import math as math


class DataFrameHandler:
    ''' Combined do-it-all handler for reading and processing all csv files relevant to family tree.

    Keyword arguments:
        first_names -- filename of first_names file.
        last_names -- filename of last_names file.
        life_expectancy -- filename of life_expectancy file.
        birth_and_marriage_rates -- filename of birth_and_marriage_rates file.
        gender_name_probability -- filename of gender_name_probability file.
    '''

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
        # normalize all the probability values such that they add to 1
        total_weight = sum(weights)
        if total_weight == 0:
            raise ValueError("List must not be empty and contents must sum to non-zero value")
        for i in range(len(weights)):
            weights[i] = weights[i] / total_weight


    # given an era, will randomly pick a gender
    def get_gender(self, era: str):
        genders = self.gender_name_probability.loc[self.gender_name_probability['decade'] == era, 'gender'].tolist()
        gender_weights = self.gender_name_probability.loc[self.gender_name_probability['decade'] == era, 'probability'].tolist()
        name_gender = random.choices(genders, weights=gender_weights, k=1)
        return name_gender[0]


    def gen_random_firstname(self, era: str) -> str:
        gender = self.get_gender(era)

        first_names = [str(x) for x in self.first_names.loc[
            (self.first_names['decade'] == era) & (self.first_names['gender'] == gender), 'name']]

        # static type checker freaks out because it doesn't know what's in the created list when we pass it to normalize weights or to choose.
        first_names_weights = [float(x) for x in
                               self.first_names.loc[(self.first_names['decade'] == era) &
                                                    (self.first_names['gender'] == gender), 'frequency']]
        # Make it so the weights all add up to 1
        self.normalize_weights(first_names_weights)
        return random.choices(first_names, weights = first_names_weights, k=1)[0]


    def gen_random_lastname(self, era: str) -> str:
        last_names = [str(x) for x in self.last_names.loc[self.last_names['Decade'] == era, 'LastName']]
        probabilities = [float(x) for x in self.rank_to_probability.columns.tolist()]
        self.normalize_weights(probabilities)

        return random.choices(last_names, weights = probabilities, k=1)[0]

    @staticmethod
    def gen_child_lastname(parent: Person) -> str:
        return parent.last_name

    def gen_year_born(self, parent: Person):
        pass



class Person():
    def __init__(self):
        self.first_name = "" # randomly generated
        self.last_name = "" # either randomly generated or passed down from the male parent
        self.gender = "" # randomly generated based on era

        self.parent = None
        self.spouse = None

        self.children = []

        self.era = -1
        self.year_born = -1
        self.year_died = -1

dfh = DataFrameHandler('first_names',
                       'last_names',
                       'life_expectancy',
                       'birth_and_marriage_rates',
                       'gender_name_probability',
                       'rank_to_probability')

#print(dfh.gen_random_firstname('1950s'))
print(dfh.gen_random_lastname('1950s'))




'''
# practice with opening and choosing a random entry from a file
df = pd.read_csv('first_names.csv')
print(type(df))
first_names = df.loc[df["decade"] == '1950s', 'name'].tolist()
first_name_weights = df.loc[df["decade"] == '1950s', 'frequency'].tolist()
print('before: ',first_name_weights)
avg_weight = sum(first_name_weights)

# normalize all the probability values such that they add to 1
for i in range(len(first_name_weights)):
    first_name_weights[i] = first_name_weights[i]/avg_weight

print('after: ',first_name_weights)

print(random.choices(first_names, weights = first_name_weights))


def round_to_nearest_decade(input):
    input /= 10
    input = math.floor(input)
    input *= 10
    print(input)
    pass

# use f-strings to assemble search strings for looking in the csv table
test = 1967
s = f"{test}s"
print(s)

round_to_nearest_decade(test)'''





"""
Loads CSV data into memory.
"""

import csv


class DataLoader:
    """Loads all CSV reference data."""

    def __init__(self):
        self.birth_marriage = {}
        self.first_names = {}
        self.gender_probability = {}
        self.last_names = []
        self.last_name_probability = []
        self.life_expectancy = {}

        self.load_all()

    def load_all(self):
        self.load_birth_marriage()
        self.load_first_names()
        self.load_gender_probability()
        self.load_last_names()
        self.load_life_expectancy()

    def load_birth_marriage(self):
        with open("birth_and_marriage_rates.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.birth_marriage[row["decade"]] = {
                    "birth_rate": float(row["birth_rate"]),
                    "marriage_rate": float(row["marriage_rate"]),
                }

    def load_first_names(self):
        with open("first_names.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row["decade"], row["gender"])
                self.first_names.setdefault(key, []).append(
                    (row["name"], float(row["frequency"]))
                )

    def load_gender_probability(self):
        with open("gender_name_probability.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.gender_probability[row["decade"]] = {
                    "male": float(row["probability"]),
                    "female": 1.0 - float(row["probability"]),
                }

    def load_last_names(self):

        # Load last names
        with open("last_names.csv") as f:
            reader = csv.DictReader(f)

            self.last_names = []

            for row in reader:
                last_name = row.get("LastName")

                if last_name and last_name.strip():
                    self.last_names.append(last_name.strip())

        # Load probabilities
        with open("rank_to_probability.csv") as f:
            reader = csv.reader(f)

            row = next(reader)

            self.last_name_probability = [
                float(x.strip())
                for x in row
                if x.strip()
            ]

        # Ensure equal length
        n = min(
            len(self.last_names),
            len(self.last_name_probability),
        )

        self.last_names = self.last_names[:n]
        self.last_name_probability = (
            self.last_name_probability[:n]
        )

        with open("rank_to_probability.csv") as f:
            reader = csv.reader(f)
            self.last_name_probability = [
                float(x) for x in next(reader)
            ]

    def load_life_expectancy(self):
        with open("life_expectancy.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = int(row["Year"])
                expectancy = float(
                    row["Period life expectancy at birth"]
                )
                self.life_expectancy[year] = expectancy
"""
Family tree generation.
"""

import random
from person import Person
from utils import decade_from_year, clamp


class TreeGenerator:
    """Generates family tree."""

    def __init__(
        self,
        tree,
        data,
        name_gen,
        life_exp,
        end_year=2120,
    ):
        self.tree = tree
        self.data = data
        self.name_gen = name_gen
        self.life_exp = life_exp
        self.end_year = end_year

    def create_person(self, year, last_name=None):
        gender = self.name_gen.generate_gender(year)

        first_name = self.name_gen.generate_first_name(
            year, gender
        )

        if not last_name:
            last_name = self.name_gen.generate_last_name()

        death_year = self.life_exp.calculate_death_year(year)

        person = Person(
            self.tree.generate_id(),
            first_name,
            last_name,
            gender,
            year,
            death_year,
        )

        self.tree.add_person(person)

        return person

    def maybe_create_partner(self, person):
        decade = decade_from_year(person.year_born)

        rate = self.data.birth_marriage[decade]["marriage_rate"]

        if random.random() < rate:
            year = person.year_born + random.randint(-10, 10)

            # Clamp to valid simulation range
            year = max(1950, min(year, self.end_year))

            partner = self.create_person(
                year,
                person.last_name,
            )

            person.set_partner(partner)
            partner.set_partner(person)

            return partner

        return None

    def create_children(self, parent1, parent2=None):
        decade = decade_from_year(parent1.year_born)

        base = self.data.birth_marriage[decade]["birth_rate"]

        minimum = int(clamp(base - 1.5, 0, 10))
        maximum = int(clamp(base + 1.5, 0, 10))

        count = random.randint(minimum, maximum)

        if parent2 is None:
            count = max(count - 1, 0)

        children = []

        start = parent1.year_born + 25
        end = parent1.year_born + 45

        for i in range(count):
            year = random.randint(start, end)

            if year > self.end_year:
                continue

            last_name = parent1.last_name

            child = self.create_person(year, last_name)

            parent1.add_child(child)
            child.parents.append(parent1)

            if parent2:
                parent2.add_child(child)
                child.parents.append(parent2)

            children.append(child)

        return children

    def generate(self):
        root1 = self.create_person(1950)
        root2 = self.create_person(1950)

        queue = [root1, root2]

        while queue:
            person = queue.pop(0)

            if person.year_born > self.end_year:
                continue

            partner = self.maybe_create_partner(person)

            children = self.create_children(person, partner)

            queue.extend(children)

        return root1, root2
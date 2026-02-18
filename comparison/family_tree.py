"""
Family Tree container and query functionality.
"""

from collections import defaultdict


class FamilyTree:
    """Stores and queries persons."""

    def __init__(self):
        self.people = {}
        self.next_id = 1

    def add_person(self, person):
        self.people[person.id] = person

    def generate_id(self):
        pid = self.next_id
        self.next_id += 1
        return pid

    def total_people(self):
        return len(self.people)

    def people_alive_by_year(self, year):
        return sum(
            1 for p in self.people.values()
            if p.is_alive_in_year(year)
        )

    def duplicate_names(self):
        counts = defaultdict(int)

        for p in self.people.values():
            counts[p.full_name] += 1

        return {
            name: count
            for name, count in counts.items()
            if count > 1
        }
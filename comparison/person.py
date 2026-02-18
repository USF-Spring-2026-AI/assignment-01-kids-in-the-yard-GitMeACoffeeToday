"""
Person class definition.
"""

from __future__ import annotations
from typing import Optional, List


class Person:
    """Represents a person in the family tree."""

    def __init__(
        self,
        person_id: int,
        first_name: str,
        last_name: str,
        gender: str,
        year_born: int,
        year_died: int,
    ):
        self.id = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.year_born = year_born
        self.year_died = year_died

        self.partner: Optional[Person] = None
        self.children: List[Person] = []
        self.parents: List[Person] = []

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def add_child(self, child: Person):
        self.children.append(child)

    def set_partner(self, partner: Person):
        self.partner = partner

    def is_alive_in_year(self, year: int) -> bool:
        return self.year_born <= year <= self.year_died

    def __repr__(self):
        return (
            f"{self.full_name} "
            f"({self.year_born}-{self.year_died})"
        )
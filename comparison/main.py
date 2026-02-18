"""
Main entry point.
"""

from data_loader import DataLoader
from family_tree import FamilyTree
from name_generator import NameGenerator
from life_expectancy import LifeExpectancy
from tree_generator import TreeGenerator


def main():

    data = DataLoader()

    tree = FamilyTree()

    name_gen = NameGenerator(data)

    life_exp = LifeExpectancy(data)

    generator = TreeGenerator(
        tree,
        data,
        name_gen,
        life_exp,
    )

    generator.generate()

    print("Total people:", tree.total_people())

    print("\nPeople alive by decade:")

    for year in range(1950, 2121, 10):
        count = tree.people_alive_by_year(year)
        print(f"{year}: {count}")

    print("Duplicate names:")
    print(tree.duplicate_names())


if __name__ == "__main__":
    main()
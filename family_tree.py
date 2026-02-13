from data_frame_handler import DataFrameHandler
from person import Person


dfh = DataFrameHandler('first_names',
                       'last_names',
                       'life_expectancy',
                       'birth_and_marriage_rates',
                       'gender_name_probability',
                       'rank_to_probability')

person1 = Person()
person1.progenitor(dfh)
print(person1.spouse.first_name)
print(f'year born: {person1.year_born}, year died: {person1.year_died}, years lived: {person1.year_died - person1.year_born}')
if person1.spouse is not None:
    print(f'year born: {person1.spouse.year_born}, year died: {person1.spouse.year_died}, years lived: {person1.spouse.year_died - person1.spouse.year_born}')
    person1.spouse.gen_marriage(dfh)


if person1.spouse is not None:
    if person1.spouse.spouse is not None:
        print(f'year born: {person1.spouse.spouse.year_born}, year died: {person1.spouse.spouse.year_died}, years lived: {person1.spouse.spouse.year_died - person1.spouse.spouse.year_born}')


print(person1.gen_children(dfh))
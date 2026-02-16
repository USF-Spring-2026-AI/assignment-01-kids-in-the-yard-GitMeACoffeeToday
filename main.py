from family_tree import build_family_tree
from person import Person
from data_frame_handler import DataFrameHandler

print('Reading files...')
dfh = DataFrameHandler('first_names',
                       'last_names',
                       'life_expectancy',
                       'birth_and_marriage_rates',
                       'gender_name_probability',
                       'rank_to_probability')

person_list = []
master_list = []
total_num_people = 0

progenitor = Person()
progenitor.progenitor(dfh)

person_list.extend(progenitor.gen_children(dfh))

master_list.append(progenitor)
master_list.extend(progenitor.gen_children(dfh))

build_family_tree(person_list, dfh, master_list)

print('Building family tree...\n')


user_input = 'None'
while user_input.lower() != 'q' and user_input.lower() != 'quit':
    print('[ Available Family Tree Options ]')
    print('(T)otal number of people')
    print('(N)ames duplicated')
    print('Total number of people by (D)ecade')
    print('> ', end='')

    user_input = input()
    if user_input.lower() == 't':
        print(f'This tree contains {tree_counter([progenitor], dfh, 0)} people.')
        print('\n')
    elif user_input.lower() == 'd':
        result = tree_name_by_decade([progenitor], dfh, {})
        for x in result:
            print(f'{x}: {result[x]}')
        print('\n')

    elif user_input.lower() == 'n':
        result = tree_find_dup_names([progenitor], dfh, {})
        has_dup = False
        for x in result:
            if result[x] > 1:
                has_dup = True
                print(f'{x}: {result[x]}')

        if not has_dup:
            print('This Tree does not contain any duplicate names.')
        print('\n')
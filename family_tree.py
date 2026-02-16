from data_frame_handler import DataFrameHandler
from person import Person

def build_family_tree(person_list: list[Person], dataframehandler: DataFrameHandler, master_list: list[Person] = None):
    """Builds the family tree recursively, master list is for printing purposes and logs all persons (spouses included via Person.spouse)"""
    if len(person_list) == 0:
        return
    else:
        person = person_list.pop(0)
        if dataframehandler.normalize_to_decade(person, 1) <= 2120:
            person.gen_marriage(dataframehandler)
            children = person.gen_children(dataframehandler)
            person_list.extend(children)

            if master_list is not None:
                master_list.extend(children)

        build_family_tree(person_list, dataframehandler, master_list)


def tree_counter(to_visit: list[Person], dataframehandler: DataFrameHandler, visited_count: int = 0) -> int:
    """Counts the number of Persons in the tree, given a progenitor person"""
    if len(to_visit) == 0:
        return visited_count
    else:
        current_person = to_visit.pop(0)
        to_visit.extend(current_person.children)
        if current_person.spouse is not None:
            return tree_counter(to_visit, dataframehandler, visited_count + 2)
        else:
            return tree_counter(to_visit, dataframehandler, visited_count + 1)


def tree_name_by_decade(to_visit: list[Person], dataframehandler: DataFrameHandler, name_decades: dict = None) -> dict:
    """Counts the number of Persons in the tree by decade."""
    if len(to_visit) == 0:
        return name_decades
    else:
        current_person = to_visit.pop(0)
        to_visit.extend(current_person.children)

        curr_decade = dataframehandler.normalize_to_decade(current_person)
        result = name_decades.get(curr_decade)
        if result is not None:
            if current_person.spouse is not None:
                name_decades[curr_decade] = result + 2
            else:
                name_decades[curr_decade] = result + 1
        else:
            if current_person.spouse is not None:
                name_decades[curr_decade] = 2
            else:
                name_decades[curr_decade] = 1

        return tree_name_by_decade(to_visit, dataframehandler, name_decades)


def tree_find_dup_names(to_visit: list[Person], dataframehandler: DataFrameHandler, dup_names: dict = None) -> dict:
    """Counts the number of Person names that repeat by decade."""
    if len(to_visit) == 0:
        return dup_names
    else:
        current_person = to_visit.pop(0)
        to_visit.extend(current_person.children)

        curr_name = current_person.first_name + ' ' + current_person.last_name
        curr_result = dup_names.get(curr_name)

        # TO-DO: Account for the spouse name as well. POTENTIAL ISSUE WITH COUNTING, DOUBLE CHECK WHEN YOU GET THE CHANCE.
        if curr_result is not None:
            dup_names[curr_name] = curr_result + 1
        else:
            dup_names[curr_name] = 1

        if current_person.spouse is not None:
            spouse_name = current_person.spouse.first_name + ' ' + current_person.spouse.last_name
            spouse_result = dup_names.get(spouse_name)
            if spouse_result is not None:
                dup_names[spouse_name] = spouse_result + 1
            else:
                dup_names[spouse_name] = 1

        return tree_find_dup_names(to_visit, dataframehandler, dup_names)

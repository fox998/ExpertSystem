
from parse_expert_data import ExpertData
from parse_expert_data import parse_expert_data

import statement

def init_from_facts(initial_facts):
    #is seams to '=ABC'?
    print(initial_facts)
    print(f'initial_facts[0] = {initial_facts[0]}')
    if not isinstance(initial_facts, str) or initial_facts[0] != '=':
        raise Exception('wrong format of initial facts')

    elif len(initial_facts) > 1:
        for fact in initial_facts[1:]:
            statement.Statements[fact] = statement.StatementValue(True)


def init_form_initial_facts_arr(initial_facts_arr):
    for initial_facts in initial_facts_arr:
        init_from_facts(initial_facts)


def fromate_implies(implies):
    implies_parts = str(implies).partition('=>')
    #is implies seams to 'C => E'?
    if not isinstance(implies, str) or len(implies_parts) != 3:
        raise Exception('wrong format of implies')
    elif len(implies_parts[2]) == 0 or len(implies_parts[0]) == 0:
        raise Exception('some part of implies is empty')
    elif '<' in implies_parts[0]:
        raise Exception('does not work with biconditional rules')

    return implies_parts

def init_from_implies_arr(implies_arr):
    for implies in implies_arr:
        implies_parts = fromate_implies(implies)
        # implies_parts ~ {'C', '=>', 'E'}. 'E' became a key and 'C' become a value
        statement.Statements[implies_parts[2]] = statement.StatementValue(implies_parts[0])



if __name__ == "__main__":
    expert_data = parse_expert_data("input.txt")
    init_form_initial_facts_arr(expert_data.initial_facts)
    init_from_implies_arr(expert_data.implies_arr)

    for key, val in statement.Statements.items():
        print(f'key: {key}, val {val.value}')



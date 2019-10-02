#!/usr/bin/env python3

from pyparsing import *

from parse_expert_data import ExpertData
from parse_expert_data import parse_expert_data

from statement import init_form_initial_facts_arr
from statement import init_from_implies_arr
from statement import StatementMap, StatementValue

from backward_chaining import is_resolvable, check_term, backward_chaining

# Tasks:
# complete open_parentheses
# add () in backward chaining

def is_queries_satisfied(Statements: dict, queries: list):
    '''Checks if we have computed all queries and have nothing to do else) '''
    c = 0
    for query in queries:
        if query in Statements.keys() and Statements[query].is_computed():
            # print(f'{query} is {Statements[query].value}')
            c = c + 1
    return (c == len(queries))


def print_result(Statements, queries):
    for query in queries:
        if query in Statements.keys() and Statements[query].is_computed():
            print(f'{query} is {Statements[query].value}')
        else:
            print(f'{query} cannot be computed with given rules.')
    return


def solve_map(Statements: dict, queries: list) -> dict:
    '''Computes rules until we have computed all of our queries.'''
    computed_keys = [fact for fact in Statements.keys() if Statements[fact].is_computed()]
    old_size = len(computed_keys)
    while not is_queries_satisfied(Statements, queries):
        uncomputed = [key for key in Statements.keys() if not Statements[key].is_computed()]
        for key in uncomputed:
            if is_resolvable(Statements[key].value, Statements):
                result = check_term(Statements[key].value, Statements)
                # print(f'check term {Statements[key].value}: {result}')
                if len(key) == 1:
                    Statements[key] = StatementValue(result)
                elif result: #????????????????????????
                    backward_chaining(Statements, key, result)
        
        computed_keys = [fact for fact in Statements.keys() if Statements[fact].is_computed()]
        if len(computed_keys) == old_size:
            break
        old_size = len(computed_keys)
        # for key, val in Statements.items():
        #     print(f'val {val.value} =>  {key}   (key)')
        # print(f'computed: {computed_keys}\n')
       
    return 


############ test stuff ###################
def test():
    expert_data = parse_expert_data("input.txt")
    init_form_initial_facts_arr(expert_data.initial_facts)
    init_from_implies_arr(expert_data.implies_arr)

    # for key, val in StatementMap.Statements.items():
    #     print(f'val {val.value} =>  {key}   (key)')

    # queries  = ['D'] # save to expert_data.queries in this format
    queries  = ['G', 'V', 'X'] 
    solve_map(StatementMap.Statements, queries)
    print_result(StatementMap.Statements, queries)

test()

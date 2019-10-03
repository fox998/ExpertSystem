#!/usr/bin/env python3

from pyparsing import *

from parse_expert_data import ExpertData
from parse_expert_data import parse_expert_data

from statement import init_form_initial_facts_arr
from statement import init_from_implies_arr
from statement import StatementMap, StatementValue

from forward_chaining import is_resolvable, check_term
from backward_chaining import backward_chaining

import sys
from functools import reduce

# Tasks:

# instantly remove !! if present

# add if not check_parentheses_order(term): 
    #     raise Exception('Wrong parentheses')

# bonus: compute all possible facts
# bonus: biconditional rules

def is_queries_satisfied(Statements: dict, queries: list):
    '''Checks if we have computed all queries and have nothing to do else) '''
    c = 0
    for query in queries:
        if query in Statements.keys() and Statements[query].is_computed():
            c = c + 1
    return (c == len(queries))


def print_result(Statements, queries):
    print(f'\nResult:')
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
        for key in list(Statements.keys()):
            if  Statements[key].is_computed():
                continue
            result = check_term(Statements[key].value, Statements)
            if result != None:
                if len(key) == 1 and result:
                    Statements[key] = StatementValue(result)
                else:
                    backward_chaining(Statements, key, result)

        computed_keys = [fact for fact in Statements.keys() if Statements[fact].is_computed()]
        if len(computed_keys) == old_size:
            break
        old_size = len(computed_keys)
        # print(f'computed: {computed_keys}\n')
        # for key, val in Statements.items():
        #     print(f'val {val.value} =>  {key}   (key)')
       
    return 


############ test stuff ###################
def test():
    expert_data = parse_expert_data(sys.argv[1])
    init_form_initial_facts_arr(expert_data.initial_facts)
    init_from_implies_arr(expert_data.implies_arr)
    
    queries_reduced = reduce(lambda x1, x2: x1+x2, expert_data.queries).replace('?', '')
    queries = set([q for q in queries_reduced])

    # for key, val in StatementMap.Statements.items():
    #     print(f'val {val.value} =>  {key}   (key)')

    solve_map(StatementMap.Statements, queries)
    print_result(StatementMap.Statements, queries)

test()

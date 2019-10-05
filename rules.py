#!/usr/bin/env python3

#from pyparsing import *

from parse_expert_data import ExpertData
from parse_expert_data import parse_expert_data

from statement import init_form_initial_facts_arr
from statement import init_from_implies_arr
from statement import StatementMap, StatementValue

from forward_chaining import check_term
from backward_chaining import backward_chaining

import sys
from functools import reduce

# Tasks:

# add if not check_parentheses_order(term): 
    #     raise Exception('Wrong parentheses')

# bonus: compute all possible facts
# bonus: biconditional rules
# explanations
# or and xor in the right part 
#

def is_queries_satisfied(Statements: dict, queries: list):
    '''Checks if we have computed all queries and have nothing to do else) '''
    c = 0
    for query in queries:
        if query in Statements.keys() and Statements[query].is_computed():
            c = c + 1
    return (c == len(queries))


def print_result(Statements, queries):
    print(f'\033[1;32;49m\nResult:')
    for query in queries:
        if query in Statements.keys() and Statements[query].is_computed():
            print(f'{query} is {Statements[query].value}')
        else:
            print(f'{query} cannot be computed with given rules. So by default {query} is False.')
    print('\033[0;37;40m')
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
            if result == True:
                if len(key) == 1 and result:
                    Statements[key] = StatementValue(result)
                else:
                    backward_chaining(Statements, key, result)

        computed_keys = [fact for fact in Statements.keys() if Statements[fact].is_computed()]
        # print(f'computed: {computed_keys}\n')
        if len(computed_keys) == old_size:
            break
        old_size = len(computed_keys)
    return 


############ test stuff ###################
def test():
    expert_data = parse_expert_data(sys.argv[1])
    init_form_initial_facts_arr(expert_data.initial_facts)
    init_from_implies_arr(expert_data.implies_arr)
    
    queries_reduced = reduce(lambda x1, x2: x1+x2, expert_data.queries).replace('?', '')
    queries = set([q for q in queries_reduced])

    print(f'queries: {queries}')
    solve_map(StatementMap.Statements, queries)
    print_result(StatementMap.Statements, queries)


test()

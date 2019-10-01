#!/usr/bin/env python3

from pyparsing import *

from parse_expert_data import ExpertData
from parse_expert_data import parse_expert_data

from statement import init_form_initial_facts_arr
from statement import init_from_implies_arr
from statement import StatementMap, StatementValue


def is_queries_satisfied(Statements: dict, queries: list):
    '''Checks if we have computed all queries and have nothing to do else) '''
    c = 0
    for query in queries:
        if query in Statements.keys() and Statements[query].is_computed():
            print(f'{query} is {Statements[query].value}')
            c = c + 1
    return (c == len(queries))


# order not -> and -> or  -> xor
def check_term(term: str, Statements: dict):
    """Checks if left part = term is true / false"""
    if '^' in term:
        term_parts = term.split('^', 1)
        return (check_term(term_parts[0], Statements) ^ check_term(term_parts[1], Statements))
    elif '|' in term:
        term_parts = term.split('|', 1)
        return (check_term(term_parts[0], Statements) or check_term(term_parts[1], Statements))
    elif '+' in term:
        term_parts = term.split('+', 1)
        return (check_term(term_parts[0], Statements) and check_term(term_parts[1], Statements))
    elif term[0] == '!':
        return not check_term(term[1:], Statements)
    return Statements[term[0]].value


def is_resolvable(term: str, Statements: dict):
    ''' Checks if left part of rule has computed literals(A, B, ...)'''
    for op in '()!+|^':
        term = term.replace(op, '')
    for literal in term:
        if literal not in Statements.keys() or not Statements[literal].is_computed():
            return False
    return True


def backward_chaining(Statements, key):
    '''Given that term is true and some variables find unknown variable.'''
    if '+' in key:
        parts = key.split('+', 1)
        return 
        # return backward_chaining()
    return


def solve_map(Statements: dict, queries: list) -> dict:
    '''Computes rules until we have computed all of our queries.'''
    computed_keys = [fact for fact in Statements.keys() if Statements[fact].is_computed()]
    print(f'computed: {computed_keys}')

    while not is_queries_satisfied(Statements, queries):
        uncomputed = [key for key in Statements.keys() if not Statements[key].is_computed()]
        for key in uncomputed:
            if is_resolvable(Statements[key].value, Statements):
                # print(f'{Statements[key].value} is OK.')
                result = check_term(Statements[key].value, Statements)
                print(f'check term {Statements[key].value}: {result}')
                if len(key) == 1:
                    Statements[key] = StatementValue(result)
                elif result:
                    backward_chaining(Statements, key)
                    pass # A+B+C => !E+G. now !E+G is true. split into parts


        break         
    return 



############ test stuff ###################
def test():
    expert_data = parse_expert_data("input.txt")
    init_form_initial_facts_arr(expert_data.initial_facts)
    init_from_implies_arr(expert_data.implies_arr)

    print(f'queries: {expert_data.queries}')
    for key, val in StatementMap.Statements.items():
        print(f'val {val.value} =>  {key}   (key)')

    queries  = ['G', 'V', 'X'] # save to expert_data.queries in this format
    solve_map(StatementMap.Statements, queries)


test()

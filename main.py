#!/usr/bin/env python3

import sys
from parse_expert_data import ExpertData
from parse_expert_data import parse_expert_data

from statement import init_form_initial_facts_arr
from statement import init_from_implies_arr
from statement import StatementMap
from statement import StatementValue

from parentheses import split_terms
from forward_chaining import do_operation

def check_queries_format(queries):
    if not isinstance(queries, str) or len(queries) < 2 or queries[0] != '?':
        raise Exception('wrong format of initial facts')


def is_operation(value: str) -> bool:
    return value in '+|^!'


def compute_statement(statement: str):
    terms_arr = split_terms(statement)
    stack = []
    i = 0
    while i < len(terms_arr): # cant use for : i can have different increment value
        if is_operation(terms_arr[i]):
            if terms_arr[i] == '!':
                stack.append(not resolve_statement(terms_arr[i+1]))
            else:
                operand1 = stack.pop()
                operand2 = resolve_statement(terms_arr[i+1])
                result = do_operation(terms_arr[i], operand1, operand2)
                stack.append(result)
            i += 1  # because we used operand = terms_arr[i+1]
        else:
            stack.append(resolve_statement(terms_arr[i]))
        i += 1
    if len(stack) != 1:
        exit(f'Error: {statement} has wrong format.')
    return stack.pop()


def resolve_statement(fact):
    print(f'resolve {fact}')
    if fact in StatementMap.Statements.keys(): # we should also check if it is a part of a key. for ex V is in !V
        value = StatementMap.Statements[fact]
        if value.is_computed():
            return value.value
        else:

            computed_value = compute_statement(value.value)
            StatementMap.Statements[fact] = computed_value
            return computed_value 

    return False


def resolve_facts(facts_arr: list):
    for fact in facts_arr:
        print(f'{fact} => {resolve_statement(fact)}')


def resolve_queries(queries_arr: list):
    for queries in queries_arr:
        check_queries_format(queries)
        # queries ~ '?GVX'
        # first char = '?', other chars are facts ~ 'GVX'
        resolve_facts(queries[1:])

    print(queries_arr)


if __name__ == "__main__":
    try:
        input_file = sys.argv[1]
    except:
        exit('\033[1;31;49mProgram takes one parameter: input file. Please provide it.\033[0;37;40m')
    expert_data = parse_expert_data(input_file)

    init_form_initial_facts_arr(expert_data.initial_facts)
    init_from_implies_arr(expert_data.implies_arr)

    for key, val in StatementMap.Statements.items():
        print(f'key: {key}, val {val.value}')

    resolve_queries(expert_data.queries)

    



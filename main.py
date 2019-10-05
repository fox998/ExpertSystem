#!/usr/bin/env python3

import sys
from parse_expert_data import ExpertData
from parse_expert_data import parse_expert_data

from statement import init_form_initial_facts_arr
from statement import init_from_implies_arr
from statement import StatementMap


def check_queries_format(queries):
    if not isinstance(queries, str) or len(queries) < 2 or queries[0] != '?':
        raise Exception('wrong format of initial facts')


def resolve_statement(fact):
    return False


def resolve_facts(facts_arr):
    for fact in facts_arr:
        print(f'{fact} => {resolve_statement(fact)}')


def resolve_queries(queries_arr):
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

    



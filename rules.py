#!/usr/bin/env python3

from pyparsing import *

from parse_expert_data import ExpertData
from parse_expert_data import parse_expert_data

from statement import init_form_initial_facts_arr
from statement import init_from_implies_arr
from statement import StatementMap


def solve_map(Statements):
    true_facts = [fact for fact in Statements.keys() if (Statements[fact].is_computed() and Statements[fact].value == True)]
    print(f'True facts: {true_facts}')

    

    return true_facts







############ test stuff ###################
def test():
    expert_data = parse_expert_data("input.txt")
    init_form_initial_facts_arr(expert_data.initial_facts)
    init_from_implies_arr(expert_data.implies_arr)
    for key, val in StatementMap.Statements.items():
        print(f'key: {key}, val {val.value}')

    true_facts = solve_map(StatementMap.Statements)


test()

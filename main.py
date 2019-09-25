
from parse_expert_data import ExpertData
from parse_expert_data import parse_expert_data

import statement

def init_form_initial_facts(initial_facts):

    for fact in initial_facts:
        if initial_facts is not str or initial_facts[0] != '=':
            raise Exception('wrong format of initial facts')
        
        elif len(initial_facts > 1):
            for fact in initial_facts[1:]:
                statement.Statements[fact] = statement.StatementValue(True)


def init_from_implies(implies_arr):
    for implies in implies_arr:
        pass



if __name__ == "__main__":
    expert_data = parse_expert_data("input.txt")
    expert_data.initial_facts



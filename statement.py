
# key is a fact name ( A, D, C ...)
# value is a StatementValue class
class StatementMap:
    Statements = dict()


class StatementValue:
    #can containe:
    #   str (as reference to another statement) and been not computed in this case
    #   bool (as end value) and been computed in this case
    def __init__(self, value):
        self.value = value

    def is_computed(self):
        return self.value is bool


def init_from_facts(initial_facts):
    #is seams to '=ABC'?
    if not isinstance(initial_facts, str) or initial_facts[0] != '=':
        raise Exception('wrong format of initial facts')

    elif len(initial_facts) > 1:
        for fact in initial_facts[1:]:
            StatementMap.Statements[fact] = StatementValue(True)


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
        # 'E' became a key and 'C' become a value
        # implies_parts ~ {'C', '=>', 'E'}.
        StatementMap.Statements[implies_parts[2]] = StatementValue(implies_parts[0])

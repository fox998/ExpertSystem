#!/usr/bin/env python3

from pyparsing import *

ops = Or(['^', '|', '+'])
fact = Optional('!') + Optional('(') + Optional('!') + Word(alphas) + Optional(')')
exp_simple = Optional('(') + fact + Optional(ops + fact)  + Optional(')')
exp = exp_simple + Optional(ops + exp_simple)
imply_rule = (exp + '=>' + exp)('implies')
equivalent_rule = (exp + '<=>' + exp)('equivalents')


def parse_rules_to_tokens(rules):
    implies_list = []
    equivalent_list = []
    for rule in rules:
        if '<=>' in rule:
            implies_list.append(imply_rule.parseString(rule))
            print(f': {implies_list[-1]}')
        else:
            equivalent_list.append(equivalent_rule.parseString(rule))




rules = ['C=>E', 'A+B+C=>D', 'A|B=>C', 'A+!B=>F', 'C|!G=>H', 'V^W=>X', 'A+B=>Y+Z', 'C|D=>X|V', 'E+F=>!V']

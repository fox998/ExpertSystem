#!/usr/bin/env python3

from statement import StatementValue
from parentheses import check_parentheses_order, split_terms
from functools import reduce

def do_operation(operation, operand1, operand2):
    if operation == '+':
        return (operand1 and operand2)
    elif operation == '|':
        return (operand1 or operand2)
    elif operation == '^':
        return (operand1 ^ operand2)


def get_literal_value(literal: str, Statements: dict):
    if literal in Statements.keys() and Statements[literal].is_computed():
        return Statements[literal].value
    return False


def check_term(term: str, Statements: dict):
    '''Checks if left part = term is true / false'''
    terms = split_terms(term)
    if len(terms) == 1 and len(terms[0]) == 1:
        return get_literal_value(terms[0], Statements)
    stack = []
    i = 0
    while i < len(terms):
        if terms[i] == '!':
            stack.append(not check_term(terms[i+1], Statements))
            i = i + 1
        elif terms[i] in '|+^':
            operand1 = stack.pop()
            operand2 = terms[i+1]
            if terms[i+1] == '!':
                operand2 += terms[i+2]
            stack.append(do_operation(terms[i], operand1, check_term(operand2, Statements)))
            i = i + 1 + int(terms[i+1] == '!')
        else:
            operand = terms[i]
            stack.append(check_term(operand, Statements))
        i = i+1
    if len(stack) != 1:
        raise Exception('Grammar error.')
    return stack[0]


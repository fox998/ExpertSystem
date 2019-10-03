#!/usr/bin/env python3

from statement import StatementValue
from parentheses import check_parentheses_order, find_close_parenthesis_ind, get_next_term
# from backward_chaining import split_terms


def do_operation(operation, operand1, operand2):
    if operation == '+':
        return (operand1 and operand2)
    elif operation == '|':
        return (operand1 or operand2)
    elif operation == '^':
        return (operand1 ^ operand2)


def is_resolvable(term: str, Statements: dict):
    ''' Checks if part of rule has computed literals(A, B, ...)'''
    for op in '()!+|^':
        term = term.replace(op, '')
    for literal in term:
        if literal not in Statements.keys() or not Statements[literal].is_computed():
            return False
    return True


def check_term(term: str, Statements: dict):
    '''Checks if left part = term is true / false'''
    if not is_resolvable(term, Statements):
        return None
    stack = []
    i = 0
    while i  < len(term):
        if len(term[i:]) == 1:
            return Statements[term[i:]].value
        if term[i] == '!':
            shift, operand = get_next_term(term[i+1:])
            stack.append(not check_term(operand, Statements))
        elif term[i] in '|+^':
            operand1 = stack.pop()
            shift, operand2 = get_next_term(term[i+1:])
            stack.append(do_operation(term[i], operand1, check_term(operand2, Statements)))
            shift = shift + 1
        elif term[i] == '(':
            end_ind = find_close_parenthesis_ind(term[i+1:])
            stack.append(check_term(term[i+1:i+end_ind+1], Statements))
            shift = end_ind + 2
        else:
            shift, operand = get_next_term(term)
            stack.append(check_term(operand, Statements))
        i = i + shift
    if len(stack) != 1:
        raise Exception('Grammar error.')
    if not isinstance(stack[0], bool):
        return Statements[stack[0]].value
    return stack[0]



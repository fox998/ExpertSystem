#!/usr/bin/env python3

from statement import StatementValue
from parentheses import check_parentheses_order, find_close_parenthesis_ind


def get_next_term(s: str):
    if s[0] not in '(!':
        return [1,  s[0]]
    if s[0] == '!':
        shift, next_term = get_next_term(s[1:])
        return [shift + 1, '!'+ next_term]
    counter = 1
    i = 0
    while counter != 0:
        i = i + 1
        if s[i] == '(':
            counter = counter + 1
        elif s[i] == ')':
            counter = counter - 1
    end_index = i
    return [len(s[:end_index+1]), s[:end_index+1]]


def do_operation(operation, operand1, operand2):
    if operation == '+':
        return (operand1 and operand2)
    elif operation == '|':
        return (operand1 or operand2)
    elif operation == '^':
        return (operand1 ^ operand2)


def check_term(term: str, Statements: dict):
    '''Checks if left part = term is true / false'''
    # if not check_parentheses_order(term): # not here, its recursive
    #     raise Exception('Wrong parentheses')
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
            # print(f'operand = {operand}, shift = {shift}')
            stack.append(check_term(operand, Statements))
        # print(f'stack = {stack}')
        # print(f'{term[i:]} ----> {term[i+shift:]}')
        i = i + shift
    if len(stack) != 1:
        raise Exception('Grammar error.')
    if not isinstance(stack[0], bool):
        return Statements[stack[0]].value
    return stack[0]



def is_resolvable(term: str, Statements: dict):
    ''' Checks if part of rule has computed literals(A, B, ...)'''
    for op in '()!+|^':
        term = term.replace(op, '')
    for literal in term:
        if literal not in Statements.keys() or not Statements[literal].is_computed():
            return False
    return True


def resolve_and(Statements, key, boolean_value):
    '''Given that key(variable) is for ex A+B and B=True,  find C'''
    parts = key.split('+', 1)
    part1, part2 = None, None
    if is_resolvable(parts[0], Statements):
        part1 = check_term(parts[0], Statements)
    if is_resolvable(parts[1], Statements):
        part2 = check_term(parts[1], Statements)
       
    if part1 == None and part2 == True:
        if len(parts[0]) == 1: 
            Statements[parts[0]] = StatementValue(True)
            print(f'As far as {key} must be {boolean_value}, and {parts[1]} is True, then {parts[0]} = True.')
        else: # then parts[0] is complex (A+B)
            backward_chaining(Statements, parts[0], True)
    elif part2 == None and part1 == True:
        if len(parts[1]) == 1:
            Statements[parts[1]] = StatementValue(True)
            print(f'As far as {key} must be {boolean_value}, and {parts[0]} is True, then {parts[1]} = True.')
        else:
            backward_chaining(Statements, parts[1], True)
    return 


# 'childish implementation'. () )))))))
def resolve_not(Statements, key, boolean_value):
    if is_resolvable(key, Statements):
        return
    print(f'As far as {key} must be {boolean_value} then {key[1:]} = {not boolean_value}.')
    backward_chaining(Statements, key[1:], not boolean_value)


def backward_chaining(Statements, key, boolean_value):
    '''Given that term is true and some variables find unknown variable.'''
    if '|' in key:
        pass
    elif '^' in key:
        pass
    elif '+' in key:
        resolve_and(Statements, key, boolean_value)
    elif '!' in key:
        resolve_not(Statements, key, boolean_value)
    elif len(key) == 1:
        Statements[key] = StatementValue(True)

    return


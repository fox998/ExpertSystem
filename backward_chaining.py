#!/usr/bin/env python3

from statement import StatementValue

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


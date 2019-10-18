#!/usr/bin/env python3

from parentheses import split_terms
from statement import StatementMap
from statement import StatementValue
from forward_chaining import do_operation


def is_operation(value: str) -> bool:
    return value in '+|^!'


def compute_statement(statement: str):
    print(f'compute statement: {statement}')
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
    print(f'statement: {statement}, stack = {stack}')
    return stack.pop()



def resolve_statement(fact):
    print(f'resolve {fact}\n')
    if fact in StatementMap.Statements.keys():
        value = StatementMap.Statements[fact]
        if value.is_computed():
            return value.value
        else:

            computed_value = compute_statement(value.value)
            StatementMap.Statements[fact] = StatementValue(computed_value)
            return computed_value 
    # also check if fact (for example V) is a part of fact (ex. V+A or !V)
    for key in StatementMap.Statements.keys():
        if fact in key:
            print(f'{fact} in {key}')
            return deduce(fact, key)
    return False



def  deduce_not(fact: str, complex_fact: str):
    value = StatementMap.Statements[complex_fact].value # no need for check: called from resolve_statement
    return not compute_statement(value)


def deduce_and(fact: str, complex_fact: str):
    return


def deduce(fact: str, complex_fact: str):
    '''Deduces fact (ex V) from complex fact(ex !V or (V+A)'''
    '''Returns bool'''
    if '|' in complex_fact:
        pass # bonus
    elif '^' in complex_fact:
        pass # bonus
    elif '+' in complex_fact:
        return deduce_and(fact, complex_fact)
    elif '!' in complex_fact: # at this point complex fact can only have letters or !
        return deduce_not(fact, complex_fact)
    return False
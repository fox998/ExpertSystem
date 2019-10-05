#!/usr/bin/env python3

from statement import StatementValue
from parentheses import check_parentheses_order, split_terms
from forward_chaining import check_term


def is_resolvable(term: str, Statements: dict):
    ''' Checks if part of rule has computed literals(A, B, ...)'''
    for op in '()!+|^':
        term = term.replace(op, '')
    for literal in term:
        if literal not in Statements.keys() or not Statements[literal].is_computed():
            return False
    return True


def backward_check(term, Statements):
    if is_resolvable(term, Statements):
        return check_term(term, Statements)
    return None


def resolve_xor(Statements, stack, boolean_value):
    ind = stack.index('^')
    left = stack[:ind]
    right = stack[ind+1:]
    op1 = backward_check(helper(left), Statements)
    op2 = backward_check(helper(right), Statements)
    if isinstance(op1, bool) and isinstance(op2, bool):
        if op1 ^ op2 != boolean_value:
            raise Exception(f'Given grammar is incorrect:{helper(left)}={op1}, \
                {helper(right)}={op2}, but {helper(left)}^{helper(right)} must be {boolean_value}')
        else:
            return
    if op1 == None and op2 == None:
        return
    if boolean_value:
        if op1 == None:
            backward_chaining(Statements, left, not op2)
            print(f'As far as {helper(left)}^{helper(right)} must be {boolean_value}, and {helper(right)} is {op2}, then {helper(left)} = {not op2}.')
        elif op2 == None:
            backward_chaining(Statements, right, not op1)
            print(f'As far as {helper(left)}^{helper(right)} must be {boolean_value}, and {helper(left)} is {op1}, then {helper(right)} = {not op1}.')
    else:
        if op1 == None:
            backward_chaining(Statements, left, op2)
            print(f'As far as {helper(left)}^{helper(right)} must be {boolean_value}, and {helper(right)} is {op2}, then {helper(left)} = {op2}.')
        elif op2 == None:
            backward_chaining(Statements, right, op1)
            print(f'As far as {helper(left)}^{helper(right)} must be {boolean_value}, and {helper(left)} is {op1}, then {helper(right)} = {op1}.')


def resolve_and(Statements, stack, boolean_value):
    '''Given that key(variable) is for ex A+B and B=True,  find C'''
    ind = stack.index('+')
    left = stack[:ind]
    right = stack[ind+1:]
    op1 = backward_check(helper(left), Statements)
    op2 = backward_check(helper(right), Statements)
    if boolean_value:
        backward_chaining(Statements, left, True)
        backward_chaining(Statements, right, True)
    elif op1 == None and op2 == True:
        backward_chaining(Statements, left, True)
        print(f'As far as {helper(left)}+{helper(right)} must be {boolean_value}, and {helper(left)} is True, then {helper(left)} = True.')
    elif op2 == None and op1 == True:
        backward_chaining(Statements, helper(right), True)
        print(f'As far as {helper(left)}+{helper(right)} must be {boolean_value}, and {helper(right)} is True, then {helper(right)} = True.')
    return 


def resolve_not(Statements, stack, boolean_value):
    operand = helper(stack[1:])
    op = backward_check(helper(operand), Statements)
    if op == None:
        print(f'As far as !{operand} must be {boolean_value} then {operand} = {not boolean_value}.')
        backward_chaining(Statements, stack[1:], not boolean_value)


def or_case_true(Statements, left, right):
    op1 = backward_check(helper(left), Statements)
    op2 = backward_check(helper(right), Statements)
    if op1 == None and op2 == None:
        return
    elif op1 == False:
        backward_chaining(Statements, right, True)
        print(f'As far as {helper(left)}|{helper(right)} and {helper(left)} is False, then {helper(right)} = True.')
    elif op2 == False:
        backward_chaining(Statements, right, True)
        print(f'As far as {helper(left)}|{helper(right)} and {helper(right)} is False, then {helper(left)} = True.')


def resolve_or(Statements, stack, boolean_value):
    ind = stack.index('|')
    left = stack[:ind]
    right = stack[ind+1:]
    if boolean_value == False:
        backward_chaining(Statements, left, False)
        backward_chaining(Statements, right, False)
    else:
        or_case_true(Statements, left, right)
        

def helper(stack):
    return  ''.join(el for el in stack)
    

def backward_chaining(Statements, stack, boolean_value):
    '''Given that term(passed like stack) is true and some variables find unknown variable.'''
    stack = split_terms(stack)
    if '|' in stack:
        resolve_or(Statements, stack, boolean_value)
    elif '^' in stack:
        resolve_xor(Statements, stack, boolean_value)
    elif '+' in stack:
        resolve_and(Statements, stack, boolean_value)
    elif '!' in stack:
        resolve_not(Statements, stack, boolean_value)
    elif len(stack) == 1:
        if len(stack[0]) == 1:
            if stack[0] in Statements.keys() and Statements[stack[0]].is_computed() and \
            Statements[stack[0]].value != boolean_value:
                exit(f'Grammar is ambiguos. Different rules imply different result for same fact.\
                    {stack[0]} = {Statements[stack[0]].value}, though another rules implies it = {boolean_value}')
            Statements[stack[0]] = StatementValue(boolean_value)
        else:
            backward_chaining(Statements, split_terms(stack[0]), boolean_value)
    return


#!/usr/bin/env python3

from statement import StatementValue
from parentheses import check_parentheses_order, split_terms
from forward_chaining import is_resolvable, check_term


def resolve_xor(Statements, stack, boolean_value):
    ind = stack.index('^')
    left = stack[:ind]
    right = stack[ind+1:]
    op1 = check_term(helper(left), Statements)
    op2 = check_term(helper(right), Statements)
    if isinstance(op1, bool) and isinstance(op2, bool):
        if op1 ^ op2 != boolean_value:
            raise Exception('Given grammar is incorrect:{left}={op1}, \
                {right}={op2}, but {left}^{right} must be {boolean_value}')
        else:
            return
    if op1 == None and op2 == None:
        return # second layer difficulty
    if boolean_value:
        if op1 == None:
            backward_chaining(Statements, left, not op2)
            print(f'As far as {left}^{right} must be {boolean_value}, and {helper(right)} is {op2}, then {helper(left)} = {not op2}.')
        elif op2 == None:
            backward_chaining(Statements, right, not op1)
            print(f'As far as {left}^{right} must be {boolean_value}, and {helper(left)} is {op1}, then {helper(right)} = {not op1}.')
    else:
        if op1 == None:
            backward_chaining(Statements, left, op2)
            print(f'As far as {left}^{right} must be {boolean_value}, and {helper(right)} is {op2}, then {helper(left)} = {not op2}.')
        elif op2 == None:
            backward_chaining(Statements, right, op1)
            print(f'As far as {left}^{right} must be {boolean_value}, and {helper(left)} is {op1}, then {helper(right)} = {op1}.')


def resolve_and(Statements, stack, boolean_value):
    '''Given that key(variable) is for ex A+B and B=True,  find C'''
    ind = stack.index('+')
    left = stack[:ind]
    right = stack[ind+1:]
    op1 = check_term(helper(left), Statements)
    op2 = check_term(helper(right), Statements)
    if op1 == None and op2 == True:
        backward_chaining(Statements, left, True)
        print(f'As far as {left}+{right} must be {boolean_value}, and {helper(left)} is True, then {helper(left)} = True.')
    elif op2 == None and op1 == True:
        backward_chaining(Statements, helper(right), True)
        print(f'As far as {left}+{right} must be {boolean_value}, and {helper(right)} is True, then {helper(right)} = True.')
    return 


def resolve_not(Statements, stack, boolean_value):
    operand = helper(stack[1:])
    op = check_term(helper(operand), Statements)
    if op != None:
        print(f'As far as !{operand} must be {boolean_value} then {operand} = {not boolean_value}.')
        backward_chaining(Statements, stack[1:], not boolean_value)


def or_case_true(Statements, left, right):
    op1 = check_term(helper(left), Statements)
    op2 = check_term(helper(right), Statements)
    if op1 == None and op2 == None:
        return
    elif op1 == False and op2 == False:
        raise Exception(f'Given grammar is incorrect: {helper(left)}={op1}, \
            {helper(right)}={op2}, but {helper(left)}+{helper(right)} must be True')
    elif op1 == False:
        backward_chaining(Statements, right, True)
        print(f'As far as {left}|{right} and {left} is False, then {right} = True.')
    elif op2 == False:
        backward_chaining(Statements, right, True)
        print(f'As far as {left}|{right} and {right} is False, then {left} = True.')



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
            Statements[stack[0]] = StatementValue(boolean_value)
        else:
            backward_chaining(Statements, split_terms(stack[0]), boolean_value)
    return


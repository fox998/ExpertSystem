#!/usr/bin/env python3

from statement import StatementValue
from parentheses import check_parentheses_order, find_close_parenthesis_ind, get_next_term
from forward_chaining import is_resolvable, check_term


def get_next_item(s: str):
    '''Used in split. Returns next operation(^+|!) , fact(A, B...) or term ((A+B)|C)...'''
    if s[0] in '!+|^' or s[0] != '(':
        return [1,  s[0]]
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


def split_terms(term: str) -> list:
    '''returns list like [A, +, (!B+(D+E)), |, F]'''
    stack = []
    i = 0
    while i < len(term):
        shift, item = get_next_item(term[i:])
        stack.append(item)
        i = i + shift
    return stack


def resolve_xor(Statements, stack, boolean_value):
    ind = stack.index('^')
    left = stack[:ind]
    right = stack[ind+1:]
    op1 = check_term(temp_helper(left), Statements)
    op2 = check_term(temp_helper(right), Statements)

    if isinstance(op1, bool) and isinstance(op2, bool):
        if op1 ^ op2 != boolean_value:
            raise Exception('Given grammar is incorrect:{left}={op1}, \
                {right}={op2}, but {left}^{right} must be {boolean_value}')
        else:
            return
         
    if op1 == None and op2 == None:
        pass # second layer difficulty

    if boolean_value:
        if op1 == None: # then op1 must be inverse to op2
            backward_chaining(Statements, left, not op2)
        elif op2 == None:
            backward_chaining(Statements, right, not op1)
    else:
        if op1 == None: # then op1 must be same as op2
            backward_chaining(Statements, left, op2)
        elif op2 == None:
            backward_chaining(Statements, right, op1)


def resolve_and(Statements, stack, boolean_value):
    '''Given that key(variable) is for ex A+B and B=True,  find C'''
    ind = stack.index('+')
    left = stack[:ind]
    right = stack[ind+1:]
    op1 = check_term(temp_helper(left), Statements)
    op2 = check_term(temp_helper(right), Statements)
       
    if op1 == None and op2 == True:
        if len(temp_helper(left)) == 1: 
            Statements[temp_helper(left)] = StatementValue(True)
            print(f'As far as {temp_helper(stack)} must be {boolean_value}, and {temp_helper(left)} is True, then {temp_helper(left)} = True.')
        else: # then parts[0] is complex (A+B)
            backward_chaining(Statements, left, True)
    elif op2 == None and op1 == True:
        if len(temp_helper(right)) == 1:
            Statements[temp_helper(right)] = StatementValue(True)
            print(f'As far as {temp_helper(stack)} must be {boolean_value}, and {temp_helper(right)} is True, then {temp_helper(right)} = True.')
        else:
            backward_chaining(Statements, temp_helper(right), True)
    return 


def resolve_not(Statements, key, boolean_value):
    if is_resolvable(key, Statements):
        return
    print(f'As far as {key} must be {boolean_value} then {key[1:]} = {not boolean_value}.')
    backward_chaining(Statements, key[1:], not boolean_value)


def or_case_true(Statements, left, right):
    op1, op2 = None, None
    if is_resolvable(temp_helper(left), Statements):
        op1 = check_term(temp_helper(left), Statements)
    if is_resolvable(temp_helper(right), Statements):
        op2 = check_term(temp_helper(right), Statements)
    if op1 == None and op2 == None:
        return
    elif op1 == False and op2 == False:
        raise Exception('Given grammar is incorrect:{left}={op1}, \
            {right}={op2}, but {left}|{right} must be {boolean_value}')
    elif op1 == False:
        backward_chaining(Statements, right, True)
    elif op2 == False:
        backward_chaining(Statements, right, True)


def resolve_or(Statements, stack, boolean_value):
    ind = stack.index('|')
    left = stack[:ind]
    right = stack[ind+1:]
    if boolean_value == False:
        backward_chaining(Statements, left, False)
        backward_chaining(Statements, right, False)
    else:
        or_case_true(Statements, left, right)
        

def temp_helper(stack):
    return  ''.join(el for el in stack)
    

def backward_chaining(Statements, stack, boolean_value): # mb instead of key just pass stack ?
    '''Given that term(passed like stack) is true and some variables find unknown variable.'''
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


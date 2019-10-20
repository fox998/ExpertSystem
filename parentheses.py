#!/usr/bin/env python3


from functools import reduce


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


# operations order: NOT > XOR > AND > OR 
def check_operations_order(stack: list) -> list:
    priority_dict = {'^': 1, '+': 2, '|': 3}
    operations_list = [el for el in stack if el in '+|^']
    order = [priority_dict[el] for el in stack if el in '+|^']
    if sorted(order) == order:
        return stack

    corrected_stack = []
    operation = operations_list[order.index(min(order))]
    ind = stack.index(operation)
    corrected_stack.append( reduce(lambda x1, x2: x1+x2, stack[:ind]) )
    corrected_stack.append(operation)
    corrected_stack.append( reduce(lambda x1, x2: x1+x2, stack[ind+1:]) )
    return corrected_stack


def split_terms(term: str) -> list:
    '''returns list like [A, +, (!B+(D+E)), |, F]'''
    stack = []
    i = 0
    while i < len(term):
        shift, item = get_next_item(term[i:])
        if item[0] == '(' and item[-1] == ')' and check_parentheses_order(item[1:-1]):
            item = item[1:-1]
        
        if len(stack) > 2 and stack[-2] in '+^|' and stack[-1] == '!':
            stack[-1] = '!' + item
        else:
            stack.append(item)
        i = i + shift
    stack = check_operations_order(stack)
    return stack


def check_parentheses_order(term: str): 
    c = 0
    for a in term: 
        if a == '(': 
            c = c + 1
        elif a == ')': 
            c = c - 1
        if c < 0:
            return False
    return (c == 0)


def test():
    s = 'A|B+C'
    print(f'{s} = {split_terms(s)}')
    print(f'{s} = {check_operations_order(s)}')
    s = '!A+B'
    print(f'{s} = {split_terms(s)}')
    s = 'A+!B'
    print(f'{s} = {split_terms(s)}')
    s = '!A'
    print(f'{s} = {split_terms(s)}')
    s = 'A^B+C|D'
    print(f'{s} = {split_terms(s)}')
    s = '!A^!B|!D+!E^U'
    print(f'{s} = {split_terms(s)}')


# test()
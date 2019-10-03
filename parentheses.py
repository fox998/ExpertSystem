#!/usr/bin/env python3

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
        if item[0] == '(' and item[-1] == ')' and check_parentheses_order(item[1:-1]):
            item = item[1:-1]
        stack.append(item)
        i = i + shift
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
    s = '(A+((!B+D)+E)|F)'
    print(f'{s} - {split_terms(s)}')
    s = '(A)|F'
    print(f'{s} - {split_terms(s)}')
    s = 'A'
    print(f'{s} - {split_terms(s)}')
    s = '(B^C)'
    print(f'{s} - {split_terms(s)}')

# test()
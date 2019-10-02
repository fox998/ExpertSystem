#!/usr/bin/env python3

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


def find_close_parenthesis_ind(s: str):
    counter = 1
    i = 0
    while counter != 0:
        i = i + 1
        if s[i] == '(':
            counter = counter + 1
        elif s[i] == ')':
            counter = counter - 1
    return i


def find_outer_indexes(term: str):
    start_ind = term.find('(')
    c = 1
    ind = start_ind + 1
    while c != 0:
        if term[ind] == '(':
            c = c+1
        elif term[ind] == ')':
            c = c-1
        ind = ind + 1
    return [start_ind, ind]


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


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
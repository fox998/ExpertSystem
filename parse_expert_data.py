class ExpertData:
    def __init__(self):
        self.implies_arr = []
        self.initial_facts = []
        self.queries = []

def format_line(line):
    line = line[:line.find('#')]
    line = line.replace(' ', '')
    return line

def get_formated_lines(lines_arr):
    return [format_line(line) for line in lines_arr]


def parse_expert_data(file):
    f = open(file,"r+")
    
    lines = [line for line in get_formated_lines(f.readlines()) if len(line) > 0]
    
    data = ExpertData()
    data.implies_arr = [line for line in lines if line[0] not in '=?']
    data.initial_facts = [line for line in lines if line[0]  == '=']
    data.queries = [line for line in lines if line[0]  == '?']
    return data
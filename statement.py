
# key is a fact name ( A, D, C ...)
# value is a StatementValue class
Statements = dict()

class StatementValue:
    #can containe:
    #   str (as reference to another statement) and been not computed in this case
    #   bool (as end value) and been computed in this case
    def __init__(self, value):
        self.value = value

    def is_computed(self):
        return self.value is bool
import enum

class SolutionType(enum.Enum):
    py3 = 1
    c = 2
    cpp = 3
    go = 4

class Solution():
    def __init__(self, programCode, tests, id):
        self.programCode = programCode
        self.tests = tests
        self.id = id
        self.solutionType = SolutionType.py3
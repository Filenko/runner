import enum

class NoSuchProgramExtensionError(Exception):
    def __init__(self, message):
        super().__init__(message)

class SolutionType(enum.Enum):
    py3 = 1
    c = 2
    cpp = 3

extensionToSolutionType = {
    "py" : SolutionType.py3,
    "cpp" : SolutionType.cpp,
    "c" : SolutionType.c
}

solutionTypeToExtension = {
    SolutionType.py3: "py",
    SolutionType.cpp: "cpp",
    SolutionType.c: "c"
}

def getSolutionType (filename) -> SolutionType:
    fileExtension = filename.split(".")[-1]
    if fileExtension in extensionToSolutionType:
        return extensionToSolutionType[fileExtension]
    else:
        raise NoSuchProgramExtensionError("No such program type!")

class Solution():
    def __init__(self, programCode, tests, id, solutionType):
        self.programCode = programCode
        self.tests = tests
        self.id = id
        self.solutionType = solutionType
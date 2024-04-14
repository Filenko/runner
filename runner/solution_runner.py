from .loader import Loader
from .solution import Solution
import asyncio
from .solution import SolutionType, solutionTypeToExtension
import runner.proto.run_pb2 as run_pb2
import enum
import json
import logging

logger = logging.getLogger("solution_runner")

class StatusCode(enum.Enum):
    OK = 1,
    TL = 2,
    ML = 3

class SolutionRunner():
    def __init__(self, container, solutionType : SolutionType):
        self.results = []
        self.container = container
        self.loader = Loader(container, solutionType)
        self.solutionType = solutionType
    async def RunProgram(self, program, test):
        await self.loader.ClearRunningDirectory()
        await self.loader.LoadProgramWithTest(program, test)
        res = await asyncio.to_thread(self.container.exec_run, f"python3 /home/runner/runner.py --prog-path /home/run/prog.{solutionTypeToExtension[self.solutionType]} --test-path /home/run/test.in", user = "run")
        res = json.loads(res.output.decode()[:-1])
        return res["status"], res["result"]

    async def RunSolution(self, solution: Solution):
        for i, test in enumerate(solution.tests):
            logger.debug(f"Run solution {solution.id} on test {i}")
            rawResult = await self.RunProgram(solution.programCode, test)
            result = run_pb2.Result(status=rawResult[0], result=rawResult[1])
            self.results.append(result)



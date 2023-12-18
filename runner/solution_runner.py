from .loader import Loader
from .solution import Solution
import asyncio

class SolutionRunner():
    def __init__(self, container):
        self.results = []
        self.container = container
        self.loader = Loader(container)
    async def RunProgram(self, program, test):
        await self.loader.ClearRunningDirectory()
        await self.loader.LoadProgram(program)
        await self.loader.LoadTest(test)
        res = await asyncio.to_thread(self.container.exec_run, f"python3 /home/runner/runner.py --prog-path /home/run/prog.py --test-path /home/run/test.in", user = "run")
        return res.output.decode()

    async def RunSolution(self, solution: Solution):
        for test in solution.tests:
            self.results.append(await self.RunProgram(solution.programCode, test))
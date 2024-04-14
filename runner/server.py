import grpc
from concurrent import futures
import runner.proto.run_pb2 as run_pb2
import runner.proto.run_pb2_grpc as run_pb2_grpc
import asyncio
import logging
import psutil
from .solution import Solution, NoSuchProgramExtensionError, getSolutionType
from .solution_runner import SolutionRunner
from .container_manager import ContainerManager, maxContainersForSolutionType
import signal

logger = logging.getLogger("server")

class Runner(run_pb2_grpc.RunnerServicer):

    async def CheckProgram(
            self,
            request: run_pb2.CodeWithTests,
            context: grpc.aio.ServicerContext,
    ) -> run_pb2.CheckResults:

        try:
            solutionType = getSolutionType(request.filename)
        except NoSuchProgramExtensionError:
            logger.debug(f"Get solution: {request.id} with unknown type")
            return run_pb2.CheckResults(status="No such program extension!")

        logger.debug(f"Get solution: {request.id} with type {solutionType.name}")

        solution = Solution(request.program_code.decode(), request.tests, request.id, solutionType)
        container = await container_manager.GetContainer(solutionType)
        logger.debug(f"Containers queue size for type {solutionType.name} is {container_manager.containers[solutionType].qsize()} with max {maxContainersForSolutionType[solutionType]}")
        runner = SolutionRunner(container, solutionType)
        await runner.RunSolution(solution=solution)
        await container_manager.PutContainer(container, solutionType)
        load_info = run_pb2.LoadInfo(free_containers=container_manager.containers[solutionType].qsize(), cpu_load=int(psutil.cpu_percent()))
        return run_pb2.CheckResults(id = solution.id, result = runner.results, load_info=load_info, status="OK!")

async def serve(port) -> None:
    global container_manager
    container_manager = await ContainerManager().init()

    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    run_pb2_grpc.add_RunnerServicer_to_server(Runner(), server)
    server.add_insecure_port(f'[::]:{port}')
    await server.start()
    logger.debug(f"Server started at port {port}")
    await server.wait_for_termination()

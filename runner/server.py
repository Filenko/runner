import grpc
from concurrent import futures
import runner.proto.run_pb2 as run_pb2
import runner.proto.run_pb2_grpc as run_pb2_grpc
import asyncio
import logging
import psutil
from .solution import Solution
from .solution_runner import SolutionRunner
from .container_manager import ContainerManager


logger = logging.getLogger("my_logger")
logging.basicConfig(level=logging.INFO, format="%(message)s")



class Runner(run_pb2_grpc.RunnerServicer):
    async def CheckProgram(
            self,
            request: run_pb2.CodeWithTests,
            context: grpc.aio.ServicerContext,
    ) -> run_pb2.CheckResults:
        solution = Solution(request.program_code.decode(), request.tests, request.id)
        print("QUEUE SIZE:", container_manager.containers.qsize())
        container = await container_manager.GetContainer()
        runner = SolutionRunner(container)
        await runner.RunSolution(solution=solution)
        await container_manager.PutContainer(container)
        load_info = run_pb2.LoadInfo(free_containers=container_manager.containers.qsize(), cpu_load=int(psutil.cpu_percent()))
        return run_pb2.CheckResults(id = solution.id, result = runner.results, load_info=load_info)

async def serve(port) -> None:
    global container_manager
    container_manager = ContainerManager()
    container_manager.RunContainers(10)
    # server = grpc.aio.server()
    # run_pb2_grpc.add_RunnerServicer_to_server(Runner(), server)
    # listen_addr = "[::]:5050"
    # server.add_insecure_port(listen_addr)
    # logging.info("Starting server on %s", listen_addr)
    # await server.start()
    # await server.wait_for_termination()

    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    run_pb2_grpc.add_RunnerServicer_to_server(Runner(), server)
    server.add_insecure_port(f'[::]:{port}')
    await server.start()
    await server.wait_for_termination()



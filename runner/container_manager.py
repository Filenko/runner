import random
import docker
import os
import asyncio

class ContainerManager():
    def __init__(self):
        self.dirPath = os.path.dirname(os.path.realpath(__file__))
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.containers = asyncio.Queue()

    async def GetContainer(self):
        return await self.containers.get()
    async def PutContainer(self, container):
        self.containers.put_nowait(container)

    def RunContainers(self, num = 10):
        if len(self.client.containers.list()) >= num:
            for container in self.client.containers.list():
                self.containers.put_nowait(container)
        else:
            for i in range(num):
                self.client.images.build(tag = "hw_py3", path = f"{self.dirPath}/docker_files/py3")
                container = self.client.containers.run(
                    image="hw_py3",
                    detach=True,
                    remove=False,
                    tty=True,
                    stdin_open=True,
                    cpu_count = 1,
                    mem_limit = "256m",
                    name = f"worker_py3_{i}",
                    network_disabled = True,
                )
                self.containers.put_nowait(container)

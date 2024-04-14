import asyncio
import docker
import os
from .solution import SolutionType
import logging

logger = logging.getLogger("container_manager")

maxContainersForSolutionType = {
    SolutionType.py3 : 1,
    SolutionType.cpp: 1,
    SolutionType.c: 1
}

class ContainerManager():
    async def init(self):
        self.dirPath = os.path.dirname(os.path.realpath(__file__))
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        await self.BuildAllImages()
        logger.debug("Build images for all types of solutions")
        self.containers = {}
        self.currentContainersRunForSolutionType = {}
        for solutionType in SolutionType:
            existingContainers = await self.GetExistingContainers(solutionType)
            logger.debug(f"Get all existing containers for {solutionType.name}, num: {len(existingContainers)}")
            self.containers[solutionType] = asyncio.Queue()
            for container in existingContainers:
                await self.containers[solutionType].put(container)
            self.currentContainersRunForSolutionType[solutionType] = len(existingContainers)
        return self

    async def GetContainer(self, solutionType : SolutionType):
        if not self.containers[solutionType].empty() \
            or (self.currentContainersRunForSolutionType[solutionType] >= maxContainersForSolutionType[solutionType]):
            return await self.containers[solutionType].get()
        else:
            container = await self.RunContainer(solutionType)
            self.currentContainersRunForSolutionType[solutionType] += 1
            logger.debug(f"Run container for {solutionType.name}, now its {self.currentContainersRunForSolutionType[solutionType]} with max {maxContainersForSolutionType[solutionType]}")
            return container


    async def PutContainer(self, container: docker.models.containers.Container, solutionType : SolutionType):
        await self.containers[solutionType].put(container)

    async def GetExistingContainers(self, solutionType : SolutionType):
        existing_containers = await asyncio.to_thread(self.client.containers.list)
        existing_containers = list(filter(lambda container: container.image, existing_containers))
        existing_containers = list(filter(lambda container: f"hw_{solutionType.value}" in container.image.attrs['RepoTags'][0], existing_containers))
        return existing_containers[:maxContainersForSolutionType[solutionType]]

    async def BuildAllImages(self):
        for solutionType in SolutionType:
            await asyncio.to_thread(self.client.images.build, tag=f"hw_{solutionType.value}", path=f"{self.dirPath}/docker_files/{solutionType.value}")\

    async def RunContainer(self, solutionType : SolutionType):
        container = await asyncio.to_thread(self.client.containers.run,
                                            image=f"hw_{solutionType.value}",
                                            detach=True,
                                            remove=False,
                                            tty=True,
                                            stdin_open=True,
                                            cpu_count=2,
                                            mem_limit="256m",
                                            network_disabled=True)
        return container

import os
import shutil
import tempfile
import tarfile
import subprocess
import asyncio
from io import BytesIO
import docker
from .solution import SolutionType, solutionTypeToExtension


class Loader():
    def __init__(self, container, solutionType : SolutionType):
        self.path = "/home/run"
        self.container = container
        self.solutionType = solutionType

    async def SaveStringsAsFilesToContainer(self, files):
        def create_tar_archive():
            tarData = BytesIO()
            with tarfile.open(fileobj=tarData, mode="w") as tar:
                for file_name, file_content in files.items():
                    fileData = BytesIO(file_content.encode('utf-8'))
                    tarInfo = tarfile.TarInfo(name=file_name)
                    tarInfo.size = len(fileData.getbuffer())
                    tar.addfile(tarinfo=tarInfo, fileobj=fileData)
            tarData.seek(0)
            return tarData.getvalue()

        tarDataValue = await asyncio.to_thread(create_tar_archive)


        await asyncio.to_thread(self.container.put_archive, "/home/run/", tarDataValue)
        await asyncio.to_thread(self.container.exec_run, f"chown -R run:run /home/run", user = "root")

    async def LoadProgramWithTest(self, program, test):
        files = {
            f"prog.{solutionTypeToExtension[self.solutionType]}": program,
            "test.in": test
        }
        await self.SaveStringsAsFilesToContainer(files)

    async def ClearRunningDirectory(self):
        await asyncio.to_thread(self.container.exec_run, f"rm -rf /home/run/*", user = "root")
        # await asyncio.to_thread(self.container.exec_run, f"rm -rf /tmp/*", user = "root")
        # await asyncio.to_thread(self.container.exec_run, f"rm -rf /var/tmp/*", user = "root")

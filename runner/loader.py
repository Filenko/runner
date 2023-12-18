import os
import shutil
import tempfile
import tarfile
import subprocess
import asyncio

class Loader():
    def __init__(self, container):
        self.path = "/home/run"
        self.container = container

    async def SaveStringAsFileToContainer(self, inputString, fileName):
        tmpFile = tempfile.NamedTemporaryFile()
        with open (tmpFile.name, "w") as f:
            f.write(inputString)
        os.chdir(os.path.dirname(tmpFile.name))
        srcname = os.path.basename(tmpFile.name)
        tar = tarfile.open(tmpFile.name + '.tar', mode='w')
        try:
            tar.add(srcname)
        finally:
            tar.close()
        data = open(tmpFile.name + '.tar', 'rb').read()
        self.container.put_archive("/home/run/", data)
        tmpFileName = tmpFile.name.split("/")[-1]
        await asyncio.to_thread(self.container.exec_run, f"mv /home/run/{tmpFileName} /home/run/{fileName}", user = "root")
        await asyncio.to_thread(self.container.exec_run, f"chown -R run:run /home/run", user = "root")
        os.remove(tmpFile.name + '.tar')
        tmpFile.close()
        return tmpFileName

    async def LoadTest(self, test):
        await self.SaveStringAsFileToContainer(test, "test.in")
    async def LoadProgram(self, program):
        await self.SaveStringAsFileToContainer(program, "prog.py")

    async def ClearRunningDirectory(self):
        await asyncio.to_thread(self.container.exec_run, f"rm -rf /home/run/*", user = "root")
        await asyncio.to_thread(self.container.exec_run, f"rm -rf /tmp/*", user = "root")
        await asyncio.to_thread(self.container.exec_run, f"rm -rf /var/tmp/*", user = "root")
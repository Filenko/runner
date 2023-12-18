import resource
import subprocess
import os

def setlimits_linux():
    resource.setrlimit(resource.RLIMIT_CPU, (1, 1))
    resource.setrlimit(resource.RLIMIT_NPROC, (0, 0))
    resource.setrlimit(resource.RLIMIT_STACK, (1024 * 1024, 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_NOFILE, (30, 30))


class Executor():
    def __init__(self):
        self.path = "/home/run"

    def Py3Execute(self):
        progPath = os.path.join(self.path, "prog.py")
        testPath = os.path.join(self.path, "test.in")

        with open(testPath, encoding="utf-8") as f_in:
            try:
                result = subprocess.Popen(
                    ["python3", progPath],
                    stdout=subprocess.PIPE,
                    stdin=f_in,
                    encoding="utf-8",
                    preexec_fn=setlimits_linux,
                    user="run"
                )
                with open("result", "w") as r:
                    return result.stdout.read()
            except subprocess.TimeoutExpired as time_limit:
                print("Time Limit!")
                return subprocess.TimeoutExpired
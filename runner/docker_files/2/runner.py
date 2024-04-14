import subprocess
import resource
import click
import time
import psutil
import enum
import json

class StatusCode(enum.Enum):
    OK = 1,
    TL = 2,
    ML = 3


def ComplileProgram (progPath):
    compile_command = ["gcc", "-o", "/home/run/1", "/home/run/prog.cpp"]
    compile_result = subprocess.run(compile_command)
    return "1"


def RunProgram(progPath, testPath, time_limit = 100, memory_limit = 1024 * 1024 * 1024):
    with open(testPath, encoding="utf-8") as f_in:
        process = subprocess.Popen(
            [f"./{progPath}"],
            stdout=subprocess.PIPE,
            stdin=f_in,
            encoding="utf-8",
            restore_signals=True
        )
        start_time = time.time()

        ps_process = psutil.Process(process.pid)

        try:
            while process.poll() is None:
                if ps_process.memory_full_info().rss > memory_limit:
                    process.kill()
                    return StatusCode.ML, None
                if time.time() - start_time > time_limit:
                    process.kill()
                    return StatusCode.TL, None
                time.sleep(0.1)
        except psutil.NoSuchProcess:
            print("Процесс завершился")

        output = process.stdout.read()

        return StatusCode.OK, output


@click.command()
@click.option(
    '--prog-path',
    help = "Path to program to execute",
    required = True
)
@click.option(
    '--test-path',
    help='Path to test for program',
    required = True
)
def main (prog_path, test_path):
    prog_path = ComplileProgram(progPath=prog_path)
    result = RunProgram(prog_path, test_path)
    result = {
        'status': result[0].name,
        'result': result[1]
    }
    print(json.dumps(result), sep = "")

if __name__ == "__main__":
    main()


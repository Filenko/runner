import subprocess
import resource
import click
import time
import psutil
import enum

class StatusCode(enum.Enum):
    OK = 1,
    TL = 2,
    ML = 3

def RunProgram(progPath, testPath, time_limit = 100, memory_limit = 1024 * 1024 * 1024):
    with open(testPath, encoding="utf-8") as f_in:
        process = subprocess.Popen(
            ["python3", progPath],
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
        print(output, sep = "")

        # with open("result", "w", encoding="utf-8") as r:
        #     r.write(output)

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
    a = RunProgram(progPath=prog_path, testPath=test_path)
    # print(a)
    return a

if __name__ == "__main__":
    main()


import asyncio
from .server import serve
import click
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(message)s')

logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('docker').setLevel(logging.CRITICAL)
logging.getLogger('asyncio').setLevel(logging.CRITICAL)
logging.getLogger('grpc').setLevel(logging.CRITICAL)


@click.command()
@click.option(
    'port',
    '--port',
    required=True,
    type=click.INT,
)
@click.command()
@click.option(
    'python_containers',
    '--python-containers',
    required=False,
    type=click.INT,
)
@click.command()
@click.option(
    'c_containers',
    '--c-containers',
    required=False,
    type=click.INT,
)
@click.command()
@click.option(
    'cpp_containers',
    '--cpp-containers',
    required=False,
    type=click.INT,
)
def main(port, python_containers, c_containers, cpp_containers):
    asyncio.run(serve(port, python_containers, c_containers, cpp_containers))

if __name__ == "__main__":
    main()
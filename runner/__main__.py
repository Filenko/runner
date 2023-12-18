import asyncio
from .server import serve
from .loader import Loader
from .container_manager import ContainerManager
import click

@click.command()
@click.option(
    'port',
    '--port',
    required=True,
    type=click.INT,
)
def main(port):
    asyncio.run(serve(port))
    print(55)

if __name__ == "__main__":
    main()
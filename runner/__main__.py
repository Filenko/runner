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
def main(port):
    asyncio.run(serve(port))

if __name__ == "__main__":
    main()
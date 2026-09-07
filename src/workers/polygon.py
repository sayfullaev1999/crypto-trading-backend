import asyncio

from core.containers import worker_container
from integrations.polygon.worker import PolygonWorker


async def main():
    async with worker_container() as scope:
        worker = await scope.get(PolygonWorker)
        await worker.run()


if __name__ == '__main__':
    asyncio.run(main())

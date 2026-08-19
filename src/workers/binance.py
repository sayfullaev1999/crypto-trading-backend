import asyncio

from core.containers import worker_container
from integrations.binance.worker import BinanceWorker


async def main():
    async with worker_container() as scope:
        worker = await scope.get(BinanceWorker)
        await worker.run()


if __name__ == '__main__':
    asyncio.run(main())

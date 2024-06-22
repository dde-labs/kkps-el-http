import os
import asyncio

from dotenv import load_dotenv
import aiohttp

from models import DelistedComp, HistDevidend
from db import insert_bulk_delisted_comp, insert_bulk_hist_devidends


load_dotenv()
FMP_API_TOKEN: str = os.getenv('FMP_API_TOKEN')
FMP_BASE_URL: str = 'https://financialmodelingprep.com/api/v3'


async def hist_devidends_task(session: aiohttp.ClientSession, symbol: str):
    async with session.get(
        f"{FMP_BASE_URL}/historical-price-full/stock_dividend/{symbol}"
        f"?apikey={FMP_API_TOKEN}"
    ) as response:
        data = await response.json()
    symbol: str = data['symbol']
    insert_bulk_hist_devidends([
        HistDevidend(symbol=symbol, **hist)
        for hist in data.get('historical', [])
    ])


async def hist_devidends(symbols: tuple[str]):
    async with aiohttp.ClientSession() as session:
        tasks = [
            hist_devidends_task(session=session, symbol=symbol)
            for symbol in symbols
        ]
        await asyncio.gather(*tasks)


async def delisted_comp():
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{FMP_BASE_URL}/delisted-companies?apikey={FMP_API_TOKEN}"
        ) as response:
            json_load = await response.json()
    insert_bulk_delisted_comp([DelistedComp(**data) for data in json_load])


async def run_all():
    SYMBOLS: tuple[str] = ('AAPL', 'AAQC',)
    res = await asyncio.gather(
        *[
            delisted_comp(),
            hist_devidends(SYMBOLS),
        ],
        return_exceptions=True,
    )
    return res


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_all())

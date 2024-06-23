import os
import asyncio

from dotenv import load_dotenv
import aiohttp

from src.models import DelistedComp, HistDevidend
from src.db import insert_bulk_delisted_comp, insert_bulk_hist_devidends


load_dotenv()
FMP_API_TOKEN: str = os.getenv('FMP_API_TOKEN')
FMP_BASE_URL: str = 'https://financialmodelingprep.com/api/v3'


async def task_hist(session: aiohttp.ClientSession, symbol: str) -> None:
    """Task for EL the Historical Dividends data that request with an input
    symbol value.
    """
    async with session.get(
        f"{FMP_BASE_URL}/historical-price-full/stock_dividend/{symbol}"
        f"?apikey={FMP_API_TOKEN}"
    ) as response:
        data = await response.json()
    symbol: str = data['symbol']
    rs: int = insert_bulk_hist_devidends((
        HistDevidend(symbol=symbol, **hist)
        for hist in data.get('historical', [])
    ))
    print(f"Success EL: Historical Dividends ({symbol}) with {rs} rows.")


async def hist_devidends(symbols: tuple[str]) -> None:
    """Multi-EL the Historical Dividends with Async"""
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            *(task_hist(session=session, symbol=symbol) for symbol in symbols)
        )


async def delisted_comp() -> None:
    """EL Delisted Companies with Async"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{FMP_BASE_URL}/delisted-companies?apikey={FMP_API_TOKEN}"
        ) as response:
            json_load = await response.json()
    rs: int = insert_bulk_delisted_comp(
        (DelistedComp(**data) for data in json_load)
    )
    print(f"Success EL: Delisted Companies with {rs} rows.")


async def run_all():
    """EL All with Async"""
    if _symbols := os.getenv('FMP_HIST_DIVID_SYMBOLS'):
        SYMBOLS: tuple[str] = tuple(s for s in _symbols.split(','))
    else:
        # Default symbols if it does not change from env var
        SYMBOLS: tuple[str] = ('AAPL', 'AAQC', 'ACP', )
    for res in await asyncio.gather(
        *[delisted_comp(), hist_devidends(SYMBOLS)], return_exceptions=True
    ):
        if res is None:
            continue
        raise res


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_all())

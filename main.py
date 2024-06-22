import os
import asyncio
import json

from dotenv import load_dotenv
import aiohttp


load_dotenv()
FMP_API_TOKEN: str = os.getenv('FMP_API_TOKEN')
FMP_BASE_URL: str = 'https://financialmodelingprep.com/api/v3'


async def hist_devidends_task(session: aiohttp.ClientSession, symbol: str):
    async with session.get(
        f"{FMP_BASE_URL}/historical-price-full/stock_dividend/{symbol}"
        f"?apikey={FMP_API_TOKEN}"
    ) as response:
        data = await response.json()
    with open(
        f'local/stock-dividend-{symbol}.json', mode='w', encoding='utf-8'
    ) as f:
        json.dump(data, f, indent=4)


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
            data = await response.json()
    with open('local/delisted-comp.json', mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    SYMBOLS: tuple[str] = ('AAPL', 'AAQC', )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        # delisted_comp(),
        hist_devidends(SYMBOLS),
    )

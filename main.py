import os
import asyncio
import json

from dotenv import load_dotenv
import aiohttp


load_dotenv()
FMP_API_TOKEN: str = os.getenv('FMP_API_TOKEN')
FMP_BASE_URL: str = 'https://financialmodelingprep.com/api/v3'


def hist_devidends():
    symbol: str = 'AAPL'
    url: str = (
        f'{FMP_BASE_URL}/historical-price-full/stock_dividend/{symbol}'
        f'?apikey={FMP_API_TOKEN}'
    )
    return url


async def delisted_comp():
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{FMP_BASE_URL}/delisted-companies?apikey={FMP_API_TOKEN}"
        ) as response:
            data = await response.json()
    with open('local/delisted-comp.json', mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delisted_comp())

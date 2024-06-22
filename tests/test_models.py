import json
from typing import Any

from models import DelistedComps, DelistedComp, HistDevidend, HistDevidends


def read_delisted_comp() -> DelistedComps:
    with open('../local/delisted-comp.json', mode='r', encoding='utf-8') as f:
        json_load: list[dict[str, Any]] = json.load(f)
    return [DelistedComp(**data) for data in json_load]


def read_hist_devidends() -> HistDevidends:
    with open(
        '../local/stock-dividend-AAPL.json', mode='r', encoding='utf-8'
    ) as f:
        data = json.load(f)
    symbol: str = data['symbol']
    return [
        HistDevidend(symbol=symbol, **hist)
        for hist in data.get('historical', [])
    ]


if __name__ == '__main__':
    read_delisted_comp()
    read_hist_devidends()

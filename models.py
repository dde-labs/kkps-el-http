from __future__ import annotations

from datetime import date as _date
from dataclasses import dataclass


@dataclass(frozen=True)
class DelistedComp:
    symbol: str
    companyName: str
    exchange: str
    ipoDate: _date
    delistedDate: _date


@dataclass()
class HistDevidend:
    symbol: str
    date: _date
    label: str
    adjDividend: float
    dividend: float
    recordDate: _date | None = None
    paymentDate: _date | None = None
    declarationDate: _date | None = None

    def __post_init__(self):
        if self.recordDate == '':
            self.recordDate: _date | None = None

        if self.paymentDate == '':
            self.paymentDate: _date | None = None

        if self.declarationDate == '':
            self.declarationDate: _date | None = None


HistDevidends = list[HistDevidend]
DelistedComps = list[DelistedComp]

from datetime import date as _date
from datetime import datetime
from dataclasses import dataclass, InitVar


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
    label: InitVar[_date]
    adjDividend: float
    dividend: float
    recordDate: _date
    paymentDate: _date
    declarationDate: _date

    def __post_init__(self, label: _date):
        if isinstance(label, str):
            self.label: _date = datetime.strptime(label, '%B %d, %y')


HistDevidends = list[HistDevidend]
DelistedComps = list[DelistedComp]

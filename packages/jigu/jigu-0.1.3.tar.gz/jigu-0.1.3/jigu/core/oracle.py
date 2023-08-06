from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Union

from jigu.core import Coin, Dec, ValAddress
from jigu.util.serdes import JsonDeserializable, JsonSerializable
from jigu.util.validation import Schemas as S
from jigu.util.validation import validate_val_address

__all__ = ["ExchangeRatePrevote", "ExchangeRateVote"]


@dataclass
class ExchangeRateVote(JsonSerializable, JsonDeserializable):

    __schema__ = S.OBJECT(
        denom=S.STRING, voter=S.VAL_ADDRESS, exchange_rate=Dec.__schema__
    )

    exchange_rate: Coin
    denom: str
    voter: ValAddress

    def __post_init__(self):
        self.voter = validate_val_address(self.voter)

    def to_data(self) -> Dict[str, Union[Dec, str, ValAddress]]:
        return {
            "exchange_rate": str(self.exchange_rate.amount),
            "denom": self.denom,
            "voter": self.voter,
        }

    @classmethod
    def from_data(cls, data) -> ExchangeRateVote:
        xr = Coin(data["denom"], data["exchange_rate"])
        return cls(exchange_rate=xr, denom=xr.denom, voter=data["voter"])


@dataclass
class ExchangeRatePrevote(JsonSerializable, JsonDeserializable):

    __schema__ = S.OBJECT(
        hash=S.STRING,
        denom=S.STRING,
        voter=S.VAL_ADDRESS,
        submit_block=S.STRING_INTEGER,
    )

    hash: str
    denom: str
    voter: ValAddress
    submit_block: int

    def __post_init__(self):
        self.voter = validate_val_address(self.voter)
        self.submit_block = int(self.submit_block)

    def to_data(self) -> Dict[str, str]:
        return {
            "hash": self.hash,
            "denom": self.denom,
            "voter": self.voter,
            "submit_block": str(self.submit_block),
        }

    @classmethod
    def from_data(cls, data: Dict[str, str]) -> ExchangeRatePrevote:
        return cls(
            hash=data["hash"],
            denom=data["denom"],
            voter=data["voter"],
            submit_block=int(data["submit_block"]),
        )

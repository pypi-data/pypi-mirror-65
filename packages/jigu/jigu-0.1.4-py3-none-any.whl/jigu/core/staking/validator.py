from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Union

from jigu.core import Coin, Dec, Timestamp, ValAddress
from jigu.core.denoms import uLuna
from jigu.util.serdes import JsonDeserializable, JsonSerializable
from jigu.util.validation import Schemas as S

__all__ = [
    "CommissionRates",
    "Commission",
    "DoNotModifyDesc",
    "Description",
    "Validator",
]


@dataclass
class CommissionRates(JsonSerializable, JsonDeserializable):

    __schema__ = S.OBJECT(
        rate=Dec.__schema__, max_rate=Dec.__schema__, max_change_rate=Dec.__schema__
    )

    rate: Dec
    max_rate: Dec
    max_change_rate: Dec

    @classmethod
    def from_data(cls, data: dict) -> CommissionRates:
        return cls(
            rate=Dec(data["rate"]),
            max_rate=Dec(data["max_rate"]),
            max_change_rate=Dec(data["max_change_rate"]),
        )


@dataclass
class Commission(JsonSerializable, JsonDeserializable):

    __schema__ = S.OBJECT(
        commission_rates=CommissionRates.__schema__, update_time=Timestamp.__schema__
    )

    rates: CommissionRates
    update_time: Timestamp

    def to_data(self) -> Dict[str, Union[CommissionRates, Timestamp]]:
        return {"commission_rates": self.rates, "update_time": self.update_time}

    @classmethod
    def from_data(cls, data: dict) -> Commission:
        return cls(
            rates=CommissionRates.from_data(data["commission_rates"]),
            update_time=Timestamp.from_data(data["update_time"]),
        )


DoNotModifyDesc = "[do-not-modify]"  # from cosmos


@dataclass
class Description(JsonSerializable, JsonDeserializable):
    __schema__ = S.OBJECT(
        moniker=S.STRING, identity=S.STRING, website=S.STRING, details=S.STRING
    )

    moniker: str = ""
    identity: str = ""
    website: str = ""
    details: str = ""

    @classmethod
    def do_not_modify(cls):
        return cls(DoNotModifyDesc, DoNotModifyDesc, DoNotModifyDesc, DoNotModifyDesc)

    @classmethod
    def from_data(cls, data) -> Description:
        return cls(data["moniker"], data["identity"], data["website"], data["details"])


@dataclass
class Validator(JsonSerializable, JsonDeserializable):

    __schema__ = S.OBJECT(
        operator_address=S.VAL_ADDRESS,
        consensus_pubkey=S.STRING,
        tokens=S.STRING_INTEGER,
        jailed=S.BOOLEAN,
        status=S.INTEGER,  # this is converted to string
        delegator_shares=Dec.__schema__,
        description=Description.__schema__,
        unbonding_height=S.STRING_INTEGER,
        unbonding_time=Timestamp.__schema__,
        commission=Commission.__schema__,
        min_self_delegation=S.STRING_INTEGER,
    )

    operator_address: ValAddress
    consensus_pubkey: str
    jailed: bool
    status_code: int
    tokens: Coin
    delegator_shares: Coin
    description: Description
    unbonding_height: int
    unbonding_time: Timestamp
    commission: Commission
    min_self_delegation: int

    @property
    def status(self) -> str:
        """String version of `status_code`"""
        return ["unbonded", "unbonding", "bonded"][self.status_code]

    def to_data(self) -> dict:
        s = self
        d = dict(self.__dict__)
        del d["status_code"]
        d["status"] = s.status_code
        d["tokens"] = str(s.tokens.amount)
        d["delegator_shares"] = str(s.delegator_shares.amount)
        d["unbonding_height"] = str(s.unbonding_height)
        d["min_self_delegation"] = str(s.min_self_delegation)
        return d

    @classmethod
    def from_data(cls, data: dict) -> Validator:
        return cls(
            operator_address=data["operator_address"],
            consensus_pubkey=data["consensus_pubkey"],
            jailed=data["jailed"],
            status_code=data["status"],
            tokens=Coin(uLuna, data["tokens"]),
            delegator_shares=Coin(uLuna, data["delegator_shares"]),
            description=Description.from_data(data["description"]),
            unbonding_height=int(data["unbonding_height"]),
            unbonding_time=Timestamp.from_data(data["unbonding_time"]),
            commission=Commission.from_data(data["commission"]),
            min_self_delegation=int(data["min_self_delegation"]),
        )

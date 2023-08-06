from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal
from typing import Callable, Dict, Generic, Iterable, List, TypeVar, Union

from jigu.error import DenomIncompatibleError
from jigu.util.serdes import JiguBox, JsonDeserializable, JsonSerializable
from jigu.util.validation import Schemas as S

from .dec import Dec

T = TypeVar("T", int, Dec)  # Amount Type

__all__ = ["Coin", "Coins"]


@dataclass(frozen=True)
class Coin(JsonSerializable, JsonDeserializable, Generic[T]):

    __schema__ = S.OBJECT(
        denom=S.STRING, amount=S.ANY(S.STRING_INTEGER, Dec.__schema__)
    )

    denom: str
    amount: T  # all get converted to int or Dec

    def __post_init__(self):
        s = self
        if (
            isinstance(s.amount, Dec)
            or isinstance(s.amount, Decimal)
            or isinstance(s.amount, float)
            or (
                isinstance(s.amount, str)
                and "." in str(s.amount)
                or "E" in str(s.amount)
            )
        ):
            object.__setattr__(
                s, "amount", Dec(s.amount)
            )  # must do this due to immutability
        else:
            try:
                object.__setattr__(s, "amount", int(s.amount))
            except ValueError:
                raise ValueError(f"unacceptable value for Coin amount: {s.amount}")

    def __repr__(self) -> str:
        return f"Coin('{self.denom}', {self.amount!r})"

    @property
    def int_coin(self) -> Coin[int]:
        return Coin(self.denom, int(self.amount))

    @property
    def dec_coin(self) -> Coin[Dec]:
        return Coin(self.denom, Dec(self.amount))

    def __str__(self) -> str:
        return f"{self.amount}{self.denom}"

    @classmethod
    def from_str(cls, string: str) -> Coin:
        pattern = r"^(\-?[0-9]+(\.[0-9]+)?)([a-zA-Z]+)$"
        match = re.match(pattern, string)
        if match:
            return cls(match.group(3), match.group(1))
        else:
            raise ValueError(f"{string} could not be parsed into Coin")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Coin):
            return self.denom == other.denom and self.amount == other.amount
        else:
            return False

    def __add__(self, other) -> Union[Coin, Coins]:
        if other == 0:
            return Coin(self.denom, self.amount)
        if isinstance(other, Coins):
            return other + self
        if not isinstance(other, Coin):
            raise TypeError(
                f"unsupported operand types for +: 'Coin' and '{type(other)}'"
            )
        if self.denom != other.denom:
            raise DenomIncompatibleError(
                f"unsupported Coin denoms for +: '{self.denom}' and '{other.denom}'"
            )
        cast = int
        if isinstance(self.amount, Dec) or isinstance(other.amount, Dec):
            cast = Dec
        return Coin(denom=self.denom, amount=cast(self.amount + other.amount))

    def __radd__(self, other) -> Union[Coin, Coins]:
        return self + other

    def __sub__(self, other: Coin) -> Coin[Union[int, Dec]]:
        if not isinstance(other, Coin):
            raise TypeError(
                f"unsupported operand types for -: 'Coin' and '{type(other)}'"
            )
        if self.denom != other.denom:
            raise DenomIncompatibleError(
                f"unsupported Coin denoms for -: '{self.denom}' and '{other.denom}'"
            )
        cast = int
        if isinstance(self.amount, Dec) or isinstance(other.amount, Dec):
            cast = Dec
        return Coin(denom=self.denom, amount=cast(self.amount - other.amount))

    def __mul__(self, other) -> Coin[T]:
        return Coin(denom=self.denom, amount=(self.amount * other))

    def __rmul__(self, other) -> Coin[T]:
        return self * other

    def __truediv__(self, other) -> Coin[T]:
        cast = type(self.amount)
        return Coin(denom=self.denom, amount=cast(self.amount / other))

    def __floordiv__(self, other) -> Coin[T]:
        cast = type(self.amount)
        return Coin(denom=self.denom, amount=cast(self.amount // other))

    def __neg__(self) -> Coin[T]:
        return Coin(denom=self.denom, amount=(-self.amount))

    def __abs__(self) -> Coin[T]:
        return Coin(denom=self.denom, amount=abs(self.amount))

    def __pos__(self) -> Coin[T]:
        return abs(self)

    def __lt__(self, other: Coin) -> bool:
        if self.denom != other.denom:
            raise DenomIncompatibleError(
                f"incompatible Coin denoms for <: '{self.denom}' and '{other.denom}'"
            )
        return self.amount < other.amount

    def __gt__(self, other: Coin) -> bool:
        if self.denom != other.denom:
            raise DenomIncompatibleError(
                f"incompatible Coin denoms for >: '{self.denom}' and '{other.denom}'"
            )
        return self.amount > other.amount

    def __ge__(self, other: Coin) -> bool:
        return self > other or self == other

    def __le__(self, other: Coin) -> bool:
        return self < other or self == other

    def to_data(self) -> dict:
        return {"denom": str(self.denom), "amount": str(self.amount)}

    def _pretty_repr_(self, path="") -> str:
        return str(self)

    @classmethod
    def from_data(cls, data: Dict[str, str]) -> Coin:
        return cls(denom=data["denom"], amount=data["amount"])


class Coins(JsonSerializable, JsonDeserializable, Generic[T]):

    __schema__ = S.ARRAY(Coin.__schema__)

    def __init__(self, coins: Iterable[Coin] = None, **denoms):
        if coins is None:
            coins = []
        coins = list(coins) + [Coin(d, a) for d, a in denoms.items()]
        self._cd = dict()
        for coin in list(coins):
            if self._cd.get(coin.denom, None) is None:
                self._cd[coin.denom] = Coin(coin.denom, coin.amount)
            else:
                self._cd[coin.denom] = coin + self._cd[coin.denom]

    def __repr__(self) -> str:
        rstr = ", ".join(f"{c.denom}={c.amount!r}" for c in self.coins)
        return f"Coins({rstr})"

    def __str__(self) -> str:
        return ", ".join(str(coin) for coin in self.coins)

    def to_data(self) -> List[Dict[str, str]]:
        return [coin.to_data() for coin in self.coins]

    def _pretty_repr_(self, path: str = "") -> str:
        d = JiguBox({coin.denom: coin.amount for coin in self.coins})
        return d._pretty_repr_()

    def __add__(self, other: Union[Coin, Coins]) -> Coins:
        if other == 0:
            return Coins(self.coins)
        elif isinstance(other, Coins):
            return Coins(self.coins + other.coins)
        elif isinstance(other, Coin):
            return Coins(self.coins + [other])
        else:
            raise TypeError(
                f"unsupported operand types for +: 'Coins' and '{type(other)}'"
            )

    def __radd__(self, other):
        return self + other

    def __mul__(self, other: Union[int, float, Decimal, Dec]) -> Coins:
        return Coins([coin * other for coin in self.coins])

    def __rmul__(self, other) -> Coins:
        return self * other

    def __truediv__(self, other: Union[int, float, Decimal, Dec]) -> Coins:
        return Coins([coin / other for coin in self.coins])

    def __floordiv__(self, other: Union[int, float, Decimal, Dec]) -> Coins:
        return Coins([coin / other for coin in self.coins])

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Coins):
            return JsonSerializable.__eq__(self, other)
        elif isinstance(other, list):
            try:
                return JsonSerializable.__eq__(self, Coins(other))
            except AttributeError:
                return False
        else:
            return False

    @classmethod
    def from_data(cls, data: List[Dict[str, str]]) -> Coins:
        coins = map(Coin.from_data, data)
        return cls(coins)

    @property
    def denoms(self) -> List[str]:
        return sorted(self._cd.keys())

    @property
    def coins(self) -> List[Coin]:
        return sorted(self._cd.values(), key=lambda c: c.denom)

    @property
    def dec_coins(self) -> Coins:
        return Coins(c.dec_coin for c in self.coins)

    @property
    def int_coins(self) -> Coins:
        return Coins(c.int_coin for c in self.coins)

    def filter(self, predicate: Callable[[Coin], bool]) -> Coins:
        return Coins(c for c in self.coins if predicate(c))

    def __iter__(self):
        return iter(self.coins)

    def __contains__(self, denom: str) -> bool:
        return denom in self._cd

    def __getitem__(self, denom: str) -> Coin:
        return self._cd[denom]

    def __getattr__(self, name: str) -> Coin:
        if name in self.denoms:
            return self[name]
        return self.__getattribute__(name)

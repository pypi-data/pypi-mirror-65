from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Any, Dict, Type

from jigu.core import Coin, Coins, Timestamp
from jigu.core.denoms import uLuna
from jigu.util.serdes import JiguBox, JsonDeserializable, JsonSerializable
from jigu.util.validation import Schemas as S

__all__ = [
    "ProposalStatus",
    "Content",
    "PROPOSAL_TYPES",
    "Proposal",
    "TextProposal",
    "ParameterChangeProposal",
    "CommunityPoolSpendProposal",
    "TaxRateUpdateProposal",
    "RewardWeightUpdateProposal",
]


class ProposalStatus(str):
    NIL = ""
    DEPOSIT_PERIOD = "DepositPeriod"
    VOTING_PERIOD = "VotingPeriod"
    PASSED = "Passed"
    REJECTED = "Rejected"
    FAILED = "Failed"


class Content(JsonSerializable, JsonDeserializable, metaclass=abc.ABCMeta):

    __schema__ = S.OBJECT(
        type=S.STRING, value=S.OBJECT(title=S.STRING, description=S.STRING)
    )

    @property
    @abc.abstractmethod
    def type(self):
        raise NotImplementedError

    def proposal_value(self):
        return dict(self.__dict__)

    def to_data(self) -> Dict[str, Any]:
        return {"type": self.type, "value": self.proposal_value()}


from .distribution import CommunityPoolSpendProposal  # isort:skip
from .gov import TextProposal  # isort:skip
from .params import ParameterChangeProposal  # isort:skip
from .treasury import RewardWeightUpdateProposal, TaxRateUpdateProposal  # isort:skip


PROPOSAL_TYPES = {
    "gov/TextProposal": TextProposal,
    "params/ParameterChangeProposal": ParameterChangeProposal,
    "distribution/CommunityPoolSpendProposal": CommunityPoolSpendProposal,
    "treasury/TaxRateUpdateProposal": TaxRateUpdateProposal,
    "treasury/RewardWeightUpdateProposal": RewardWeightUpdateProposal,
}


@dataclass
class Proposal(JsonSerializable, JsonDeserializable):

    __schema__ = S.OBJECT(
        content=Content.__schema__,
        id=S.STRING_INTEGER,
        proposal_status=S.STRING,
        final_tally_result=S.OPTIONAL(
            S.OBJECT(  # this gets marshalled into Coin
                yes=S.STRING_INTEGER,
                abstain=S.STRING_INTEGER,
                no=S.STRING_INTEGER,
                no_with_veto=S.STRING_INTEGER,
            )
        ),
        submit_time=Timestamp.__schema__,
        deposit_end_time=Timestamp.__schema__,
        total_deposit=Coins.__schema__,
        voting_start_time=Timestamp.__schema__,
        voting_end_time=Timestamp.__schema__,
    )

    content: Type[Content]
    id: int
    proposal_status: str
    final_tally_result: JiguBox[str, Coin]
    submit_time: Timestamp
    deposit_end_time: Timestamp
    total_deposit: Coins
    voting_start_time: Timestamp
    voting_end_time: Timestamp

    def to_data(self) -> dict:
        d = JiguBox(self.__dict__)
        d.id = str(d.id)
        for x in d.final_tally_result:
            d.final_tally_result[x] = d.final_tally_result[x].amount
        return d

    @property
    def pretty_data(self):
        d = dict(self.__dict__)
        proposal_id = d.pop("id")
        content = d.pop("content")
        ix = [
            ("id", proposal_id),
            ("type", content.type),
            *list(content.pretty_data),
            *list(d.items()),
        ]
        return ix

    @classmethod
    def from_data(cls, data: dict) -> Proposal:
        final_tally_result = data["final_tally_result"]
        for key in final_tally_result:
            final_tally_result[key] = Coin(uLuna, int(final_tally_result[key]))
        p_type = PROPOSAL_TYPES[data["content"]["type"]]
        content = p_type.from_data(data["content"])
        return cls(
            content=content,
            id=int(data["id"]),
            proposal_status=ProposalStatus(data["proposal_status"]),
            final_tally_result=JiguBox(final_tally_result),
            submit_time=Timestamp.from_data(data["submit_time"]),
            deposit_end_time=Timestamp.from_data(data["deposit_end_time"]),
            total_deposit=Coins.from_data(data["total_deposit"]),
            voting_start_time=Timestamp.from_data(data["voting_start_time"]),
            voting_end_time=Timestamp.from_data(data["voting_end_time"]),
        )

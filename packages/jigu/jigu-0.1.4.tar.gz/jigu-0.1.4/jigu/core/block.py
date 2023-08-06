from __future__ import annotations

from dataclasses import dataclass
from typing import List, Union

from jigu.core.auth.transaction import StdTx, TxInfo
from jigu.core.sdk import Timestamp
from jigu.query.txinfo import TxInfosQuery
from jigu.util.serdes import JiguBox, JsonDeserializable, JsonSerializable
from jigu.util.validation import Schemas as S


@dataclass
class BlockHeader(JsonSerializable, JsonDeserializable):

    __schema__ = S.OBJECT(
        block_id=S.OBJ,
        header=S.OBJECT(
            chain_id=S.STRING,
            height=S.STRING_INTEGER,
            time=Timestamp.__schema__,
            num_txs=S.STRING_INTEGER,
            total_txs=S.STRING_INTEGER,
            last_commit_hash=S.STRING,
            data_hash=S.STRING,
            next_validators_hash=S.STRING,
            consensus_hash=S.STRING,
            app_hash=S.STRING,
            proposer_address=S.STRING,
            last_block_id=S.OBJ,
        ),
    )

    chain_id: str
    height: int
    time: Timestamp
    num_txs: int
    total_txs: int
    hashes: dict
    proposer: str
    block_id: JiguBox
    last_block_id: JiguBox

    @classmethod
    def from_data(cls, data: dict) -> BlockHeader:
        header = data["header"]
        hashes = JiguBox(
            {
                "last_commit": header["last_commit_hash"],
                "data": header["data_hash"],
                "validators": header["validators_hash"],
                "next_validators": header["next_validators_hash"],
                "consensus": header["consensus_hash"],
                "app": header["app_hash"],
                "last_results": header["last_results_hash"],
                "evidence": header["evidence_hash"],
            }
        )
        return cls(
            chain_id=header["chain_id"],
            height=int(header["height"]),
            time=Timestamp.from_data(header["time"]),
            num_txs=int(header["num_txs"]),
            total_txs=int(header["total_txs"]),
            hashes=hashes,
            proposer=header["proposer_address"],
            block_id=JiguBox(data["block_id"]),
            last_block_id=JiguBox(header["last_block_id"]),
        )


# TODO: serialization currently doesn't match how it gets deserialized -- should
# we try to make it consistent? normal block fetching behavior gets txinfo instead of
# stdtx for the txs column.


@dataclass
class Block(BlockHeader, JsonDeserializable):

    __schema__ = S.OBJECT(
        block_meta=BlockHeader.__schema__,
        block=S.OBJECT(
            data=S.OBJECT(txs=S.OPTIONAL(S.ARRAY(S.STRING))),
            evidence={},
            last_commit={},
        ),
    )

    evidence: JiguBox  # TODO: improve and document
    last_commit: JiguBox  # TODO: improve and document
    txs: List[
        Union[str, StdTx, TxInfo, TxInfosQuery]
    ]  # ordered last for convenience of pretty printing

    @classmethod
    def from_data(cls, data: dict) -> Block:
        header = BlockHeader.from_data(data["block_meta"])
        txs = (
            data["block"]["data"]["txs"] or []
        )  # these will be Amino-encoded tx strings
        evidence = JiguBox(data["block"].get("evidence"))
        last_commit = JiguBox(data["block"].get("last_commit"))
        return cls(
            txs=txs, evidence=evidence, last_commit=last_commit, **header.__dict__
        )

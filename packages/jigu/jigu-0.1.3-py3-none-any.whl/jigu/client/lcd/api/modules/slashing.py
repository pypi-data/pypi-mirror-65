from typing import Optional, Union

from jigu.client.lcd.api import BaseApi, project
from jigu.core import Dec, Timestamp, ValConsPubKey
from jigu.util.serdes import JiguBox
from jigu.util.validation import (
    validate_val_consaddress,
    validate_val_conspubkey
)

__all__ = ["SlashingApi"]


def to_signing_info(si):
    box = JiguBox(
        si,
        box_recast={
            "start_height": int,
            "index_offset": int,
            # "jailed_until": Timestamp,
            "missed_blocks_counter": int,
        },
    )
    box.jailed_until = Timestamp.from_data(box.jailed_until)
    return box


# TODO: document and revamp
class SlashingApi(BaseApi):
    def signing_info_by_pubkey(self, pubkey: ValConsPubKey):
        validate_val_conspubkey(pubkey)
        res = self._api_get(f"/slashing/validators/{pubkey}/signing_info")
        return project(res, to_signing_info(res))

    def signing_info_by_address(self, address: str = None):
        validate_val_consaddress(address)
        res = self._api_get("/slashing/signing_infos")
        infos = [to_signing_info(r) for r in res]
        by_address = JiguBox({info.address: info for info in infos})
        return project(res, by_address[address] if address else by_address)

    def params(self, key: Optional[str] = None) -> Union[int, Dec, dict]:
        res = self._api_get("/slashing/parameters")
        p = JiguBox(
            res,
            box_recast={
                "max_evidence_age": int,
                "signed_blocks_window": int,
                "min_signed_per_window": Dec,
                "downtime_jail_duration": int,
                "slash_fraction_double_sign": Dec,
                "slash_fraction_downtime": Dec,
            },
        )
        return project(res, p[key] if key else p)

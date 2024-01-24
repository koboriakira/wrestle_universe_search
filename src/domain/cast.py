from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Cast:
    id: str
    displayName: str # 漢字
    type: int # "2"らしい。何を表しているかは不明
    keyVisualUrl: str # 全体像の写真
    profileImageUrl: str # 顔写真
    kanaName: str # ひらがな
    subDisplayName: str # 英語
    # profileImageBlurHash: str
    # 以下は取得できるが使わない
    # members: Any # 原則nullっぽい
    # keyVisualBlurHash: str

    @staticmethod
    def from_params(params: dict) -> 'Cast':
        return Cast(
            params["id"],
            params["displayName"],
            params["type"],
            params["keyVisualUrl"],
            params["profileImageUrl"],
            params["kanaName"],
            params["subDisplayName"],
        )

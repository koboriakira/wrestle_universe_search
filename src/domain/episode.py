import json
from dataclasses import dataclass
from domain.cast import Cast
from domain.attribute_label import AttributeLabel
from domain.video_chapter import VideoChapter
from typing import Any
import logging
logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class Episode:
    id: str
    displayName: str # 興行タイトル
    description: str # 詳細。対戦カードなどが書いてある
    keyVisualUrl: str # image/jpeg形式の画像URL。拡張子jpegは存在しない
    casts: list[Cast] # 参戦選手。どの試合にいるかはわからない
    attributeLabels: AttributeLabel # 興行に関する情報
    videoChapters: list[VideoChapter] # 各試合のチャプター情報。最新の興行だと用意されている
    # 以下は取得できるが使わない
    # labels: Any attributeLabelsと同じ情報が入っている
    # keyVisualBlurHash: str
    # alterKeyVisualBlurHash: str
    # watchStartTime: int
    # watchEndTime: int
    # duration: int
    # paidType: int
    # supportAudioLanguages: Any
    # links: Any
    # alterKeyVisualUrl: str

    @staticmethod
    def from_params(params: dict) -> 'Episode':
        casts = [Cast.from_params(c) for c in params["casts"]] if params["casts"] else []
        attributeLabels = AttributeLabel.from_params(params["attributeLabels"])
        videoChapters = [VideoChapter.from_params(v) for v in params["videoChapters"]] if params["videoChapters"] else []
        return Episode(
            params["id"],
            params["displayName"],
            params["description"],
            params["keyVisualUrl"],
            casts,
            attributeLabels,
            videoChapters
        )

    def has_chapter(self) -> bool:
        return len(self.videoChapters) > 0

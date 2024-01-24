from dataclasses import dataclass
from domain.cast import Cast
from typing import Any, Optional
import logging
import re
logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class VideoChapter:
    id: str
    start: int
    end: int
    displayName: str
    description: str
    keyVisualUrl: str
    keyVisualBlurHash: str
    casts: list[Cast]
    headline: bool

    DELIMITER_CAST = r'&|vs|\、|＆|　|＞|＜'

    @staticmethod
    def from_params(params: dict) -> 'VideoChapter':
        casts = [Cast.from_params(c) for c in params["casts"]] if params["casts"] else []
        return VideoChapter(
            params["id"],
            params["start"],
            params["end"],
            params["displayName"],
            params["description"],
            params["keyVisualUrl"],
            params["keyVisualBlurHash"],
            casts,
            params["headline"] if "headline" in params else False,
        )
    def _get_casts(self) -> list[str]:
        """ 試合タイトル(displayName)から選手名を取得する

        入力例: アジャコング & 桐生真弥 vs 中島翔子 & 上福ゆき
        出力例 ["アジャコング", "桐生真弥", "中島翔子", "上福ゆき"]
        """
        display_name = re.sub('王者|挑戦者', '', self.displayName)
        names = re.split(self.DELIMITER_CAST, display_name)
        return [name.strip() for name in names if name.strip()]

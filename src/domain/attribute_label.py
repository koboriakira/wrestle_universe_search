from dataclasses import dataclass
from typing import Any, Optional
from datetime import date as Date
import re

@dataclass(frozen=True)
class AttributeLabel:
    group: Optional[str] # 団体名
    matchDate: Optional[Date] # 興行日
    venue: Optional[str] # 興行会場

    @staticmethod
    def from_params(params: dict) -> 'AttributeLabel':
        # params["matchDate"]からYYYY-MM-DDを取得する
        match_date_str = params["matchDate"] if "matchDate" in params else None
        match_date = re.search(r'\d{4}-\d{2}-\d{2}', match_date_str).group() if match_date_str else None
        return AttributeLabel(
            params["group"] if "group" in params else None,
            Date.fromisoformat(match_date) if match_date else None,
            params["venue"] if "venue" in params else None,
        )

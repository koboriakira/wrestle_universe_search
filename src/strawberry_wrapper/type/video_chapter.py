import strawberry
from typing import Optional
from datetime import date as Date
from util.custom_logging import get_logger
from strawberry_wrapper.type.cast import Cast
logger = get_logger(__name__)

@strawberry.type
class VideoChapter:
    id: str
    display_name: str
    description: str
    key_visual_url: str
    casts: list[Cast]
    headline: str
    episode_id: Optional[str]
    match_date: Date

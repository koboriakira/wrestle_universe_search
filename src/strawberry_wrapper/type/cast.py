import strawberry
from util.custom_logging import get_logger

logger = get_logger(__name__)

@strawberry.type
class Cast:
    id: str
    display_name: str
    kana_name: str
    sub_display_name: str
    key_visual_url: str
    profile_image_url: str

from util.custom_logging import get_logger
from strawberry_wrapper.type.cast import Cast
from domain.infrastructure.json_repository import JsonRepository

logger = get_logger(__name__)

class QueryCasts:
    def __init__(self, json_repository: JsonRepository):
        self.json_repository = json_repository

    def query(self) -> list[Cast]:
        casts_json_data = self.json_repository.load_casts()
        casts = [Cast(
            id=cast["id"],
            display_name=cast["displayName"],
            kana_name=cast["kanaName"],
            sub_display_name=cast["subDisplayName"],
            key_visual_url=cast["keyVisualUrl"],
            profile_image_url=cast["profileImageUrl"],
        ) for cast in casts_json_data]
        return casts

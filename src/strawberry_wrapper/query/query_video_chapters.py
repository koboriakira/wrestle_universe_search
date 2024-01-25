from typing import Optional
from datetime import date as Date
from util.custom_logging import get_logger
from strawberry_wrapper.type import Cast, VideoChapter
from domain.infrastructure.json_repository import JsonRepository

logger = get_logger(__name__)

class QueryVideoChapters:
    def __init__(self, json_repository: JsonRepository):
        self.json_repository = json_repository

    def query(self, start: Optional[Date] = None, end: Optional[Date] = None) -> list[VideoChapter]:
        casts_json_data = self.json_repository.load_casts()
        video_chapters_json_data = self.json_repository.load_video_chapters(start=start, end=end)

        result = []
        for video_chapter in video_chapters_json_data:
            casts = [Cast(
                id=cast["id"],
                display_name=cast["displayName"],
                kana_name=cast["kanaName"],
                sub_display_name=cast["subDisplayName"],
                key_visual_url=cast["keyVisualUrl"],
                profile_image_url=cast["profileImageUrl"],
            ) for cast in casts_json_data if cast["id"] in video_chapter["casts"]]
            result.append(VideoChapter(
                id=video_chapter["id"],
                display_name=video_chapter["displayName"],
                description=video_chapter["description"],
                key_visual_url=video_chapter["keyVisualUrl"],
                casts=casts,
                headline=video_chapter["headline"],
                episode_id=video_chapter["episodeId"] if "episodeId" in video_chapter else None,
                match_date=Date.fromisoformat(video_chapter["matchDate"]),
            ))
        return result

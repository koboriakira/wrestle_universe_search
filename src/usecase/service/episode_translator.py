from typing import Optional
from util.custom_logging import get_logger

logger = get_logger(__name__)

class EpisodeTranslator:
    @classmethod
    def translate(cls, episodes: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
        all_episodes: list[dict] = []
        all_casts:list[dict] = []
        all_video_chapters:list[dict] = []
        for e in episodes:
            try:
                id = e["id"]
                display_name = e["displayName"]
                description = e["description"]
                key_visual_url = e["keyVisualUrl"]
                links = e["links"]
                url = links["other"] if "other" in links else links[0] if len(links) > 0 else None
                if "attributeLabels" in e:
                    attribute_labels = e["attributeLabels"]
                    group = attribute_labels["group"] if "group" in attribute_labels else None
                    match_date = attribute_labels["matchDate"] if "matchDate" in attribute_labels else None
                    # 最初の10文字を取得して、YYYY-MM-DD形式にする
                    match_date = match_date[:10] if match_date is not None else None
                    venue = attribute_labels["venue"] if "venue" in attribute_labels else None
                casts = e["casts"] if "casts" in e and e["casts"] else []
                cast_id_list = [c["id"] for c in casts]
                all_casts = cls.translate_casts(casts, all_casts)
                video_chapters = cls.translate_video_chapters(video_chapters=e["videoChapters"], episode_id=id, match_date=match_date) if "videoChapters" in e else []
                all_video_chapters += video_chapters
                video_chapter_id_list = [c["id"] for c in video_chapters]
                episode = {
                    "id": id,
                    "displayName": display_name,
                    "description": description,
                    "keyVisualUrl": key_visual_url,
                    "group": group,
                    "matchDate": match_date,
                    "venue": venue,
                    "casts": cast_id_list,
                    "videoChapters": video_chapter_id_list,
                    "url": url,
                }
                all_episodes.append(episode)
            except Exception as err:
                logger.error(err)
                logger.error(e)
                raise e
        return all_episodes, all_casts, all_video_chapters


    @classmethod
    def translate_casts(cls, casts: list[dict], prev_casts_list: list[dict]) -> list[dict]:
        """
        試合情報のキャスト情報を整形する
        prev_casts_listにマージして返す
        """
        prev_cast_id_list = [c["id"] for c in prev_casts_list]
        filtered_casts = [c for c in casts if c["id"] not in prev_cast_id_list]
        for cast in filtered_casts:
            id = cast["id"]
            type = cast["type"]
            display_name = cast["displayName"]
            key_visual_url = cast["keyVisualUrl"]
            kana_name = cast["kanaName"]
            sub_display_name = cast["subDisplayName"]
            profile_image_url = cast["profileImageUrl"]
            # prev_casts_listにマージする
            prev_casts_list.append({
                "id": id,
                "type": type,
                "displayName": display_name,
                "keyVisualUrl": key_visual_url,
                "kanaName": kana_name,
                "subDisplayName": sub_display_name,
                "profileImageUrl": profile_image_url,
            })
        return prev_casts_list

    @classmethod
    def translate_video_chapters(cls, video_chapters: list[dict], episode_id: str, match_date: Optional[str] = None) -> list[dict]:
        """
        試合情報のビデオチャプター情報を整形する
        """
        result = []
        for video_chapter in video_chapters:
            id = video_chapter["id"]
            display_name = video_chapter["displayName"]
            description = video_chapter["description"]
            key_visual_url = video_chapter["keyVisualUrl"]
            casts:list = video_chapter["casts"] if "casts" in video_chapter and video_chapter["casts"] else []
            headline = video_chapter["headline"]
            result.append({
                "id": id,
                "displayName": display_name,
                "description": description,
                "keyVisualUrl": key_visual_url,
                "casts": casts,
                "headline": headline,
                "episode_id": episode_id,
                "matchDate": match_date,
            })
        return result

from util.custom_logging import get_logger

logger = get_logger(__name__)

class EventTranslator:
    @classmethod
    def translate(cls, events: list[dict]) -> list[dict]:
        all_episodes: list[dict] = []
        for e in events:
            logger.info(e)
            id = e["id"]
            display_name = e["displayName"]
            description = e["description"]
            key_visual_url = e["keyVisualUrl"]
            url = e["links"]["other"]
            if "labels" in e:
                labels = e["labels"]
                group = labels["group"] if "group" in labels else None
                match_date = labels["matchDate"] if "matchDate" in labels else None
                # 最初の10文字を取得して、YYYY-MM-DD形式にする
                match_date = match_date[:10] if match_date is not None else None
                venue = labels["venue"] if "venue" in labels else None
            episode = {
                "id": id,
                "displayName": display_name,
                "description": description,
                "keyVisualUrl": key_visual_url,
                "group": group,
                "matchDate": match_date,
                "venue": venue,
                # castsとvideoChaptersは大体入っていなそうなので、空リストを入れておく
                "casts": [],
                "videoChapters": [],
                "url": url,
            }
            all_episodes.append(episode)
        return all_episodes

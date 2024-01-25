# どうせWRESTLE UNIVERSEからしか取得しないので、infrastructure層の実装もここに書いている

from typing import Optional
import requests
from util.custom_logging import get_logger

logger = get_logger(__name__)


class EventFetcher:
    BASE_URL = 'https://api.wrestle-universe.com/v1/events?al=ja&labels=tjpw-archive&pageSize=20'

    def handle(self) -> tuple[list[dict], Optional[str]]:
        """WRESTLE UNIVERSEより試合情報を取得する

        Args:
            stop_episode_id (str): 取得を終了する興行ID。この興行が含まれたら取得を終了する
            count (int): 取得する回数。この回数を超えたら取得を終了する

        Returns:
            EpisodeFetchResponse:
        """
        events, next_page_token = self._get()
        return events, next_page_token

    def _get(self) -> tuple[list[dict], Optional[str]]:
        response = requests.get(self.BASE_URL)
        data = response.json()
        nextPageToken = data["nextPageToken"] if "nextPageToken" in data else None
        return data["events"], nextPageToken

if __name__ == "__main__":
    # python -m usecase.service.event_fetcher
    fetcher = EventFetcher()
    fetcher.handle()

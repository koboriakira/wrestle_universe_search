# どうせWRESTLE UNIVERSEからしか取得しないので、infrastructure層の実装もここに書いている

from typing import Optional
import requests
import time
from util.custom_logging import get_logger

logger = get_logger(__name__)


class EpisodeFetcher:
    BASE_URL = 'https://api.wrestle-universe.com/v1/videoEpisodes?al=ja&labels=-tjpw&pageSize=20'


    def handle(self, stop_episode_id: Optional[str] = None, count: int = 5) -> list[dict]:
        """WRESTLE UNIVERSEより試合情報を取得する

        Args:
            stop_episode_id (str): 取得を終了する興行ID。この興行が含まれたら取得を終了する
            count (int): 取得する回数。この回数を超えたら取得を終了する

        Returns:
            EpisodeFetchResponse:
        """
        next_page_token = ""
        count = 0
        episodes: list[dict] = []
        while next_page_token is not None and count < 5:
            count += 1
            time.sleep(1)
            res = self._get(next_page_token)
            # episodesにres[0]を追加する
            episodes += res[0]
            next_page_token = res[1]

            # stop_episode_idが含まれていたら取得を終了する
            if stop_episode_id in [e["id"] for e in episodes]:
                break
        return episodes

    def _get(self, next_page_token: Optional[str] = None) -> tuple[list[dict], Optional[str]]:
        params = {}
        if next_page_token is not None and next_page_token != "":
            params["pageToken"] = next_page_token
        logger.info("requests.get")
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()
        nextPageToken = data["nextPageToken"] if "nextPageToken" in data else None
        return data["episodes"], nextPageToken

if __name__ == "__main__":
    # python -m usecase.service.episode_fetcher
    fetcher = EpisodeFetcher()
    # fetcher._get(EpisodeFetcher.BASE_URL)
    # fetcher.handle(stop_episode_id="sDueqz5UupTXsBsb84V2Ek")
    fetcher.handle()

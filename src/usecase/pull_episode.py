import json
import pathlib
from typing import Optional
from usecase.service.episode_fetcher import EpisodeFetcher
from usecase.service.event_fetcher import EventFetcher
from usecase.service.episode_translator import EpisodeTranslator
from usecase.service.event_translator import EventTranslator
from util.custom_logging import get_logger
from domain.infrastructure.json_repository import JsonRepository

logger = get_logger(__name__)
DEFAULT_DIR = "data"

class PullEpisodesUsecase:
    """ 興行データを収集して保存するユースケース """
    def __init__(self, repository: JsonRepository) -> None:
        self._episode_fetcher = EpisodeFetcher()
        self._event_fetcher = EventFetcher()
        self._repository = repository

    def handle(self, next_page_token: Optional[str] = None, stop_episode_id: Optional[str] = None, dir: str = DEFAULT_DIR, count: int = 1) -> str:
        """WRESTLE UNIVERSEより試合情報を取得する

        Args:
            stop_episode_id (str): 取得を終了する興行ID。この興行が含まれたら取得を終了する
            dir (str): 取得したデータを保存するディレクトリ

        Returns:
            EpisodeFetchResponse:
        """
        logger.info("get events from WRESTLE UNIVERSE")
        fetched_events, event_next_page_token = self._event_fetcher.handle()
        events = EventTranslator.translate(fetched_events)

        logger.info("get episodes from WRESTLE UNIVERSE")
        fetched_episodes, fetched_next_page_token = self._episode_fetcher.handle(next_page_token=next_page_token,
                                                        stop_episode_id=stop_episode_id,
                                                        count=count)
        logger.info("fetched_next_page_token: %s", fetched_next_page_token)
        print("fetched_next_page_token: %s", fetched_next_page_token)
        logger.info("translate episodes")
        episodes, casts, video_chapters = EpisodeTranslator.translate(fetched_episodes)

        self._repository.save_events(events)
        self._repository.save_episodes(episodes)
        self._repository.save_casts(casts)
        self._repository.save_video_chapters(video_chapters)

        return fetched_next_page_token



    def _init_if_needed(self, dir: str) -> None:
        """
        ディレクトリの初期化を行う
        """
        # dirが存在すればスキップ
        if pathlib.Path(dir).exists():
            return
        # dirが存在しなければ作成する
        pathlib.Path(dir).mkdir(parents=True, exist_ok=True)

        # jsonファイルが存在しなければ作成する
        with open(f"{dir}/episodes.json", "w") as f:
            json.dump([], f, ensure_ascii=False)
        with open(f"{dir}/casts.json", "w") as f:
            json.dump([], f, ensure_ascii=False)
        with open(f"{dir}/video_chapters.json", "w") as f:
            json.dump([], f, ensure_ascii=False)

if __name__ == "__main__":
    # python -m usecase.pull_episode
    pull_episode = PullEpisodesUsecase()
    pull_episode.handle(next_page_token=None)

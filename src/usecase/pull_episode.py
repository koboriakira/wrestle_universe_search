import json
import pathlib
from typing import Optional
from usecase.service.episode_fetcher import EpisodeFetcher
from usecase.service.episode_translator import EpisodeTranslator
from util.custom_logging import get_logger

logger = get_logger(__name__)
DEFAULT_DIR = "data"

class PullEpisodesUsecase:
    """ 興行データを収集して保存するユースケース """
    def __init__(self) -> None:
        self._episode_fetcher = EpisodeFetcher()

    def handle(self, next_page_token: Optional[str] = None, stop_episode_id: Optional[str] = None, dir: str = DEFAULT_DIR) -> None:
        """WRESTLE UNIVERSEより試合情報を取得する

        Args:
            stop_episode_id (str): 取得を終了する興行ID。この興行が含まれたら取得を終了する
            dir (str): 取得したデータを保存するディレクトリ

        Returns:
            EpisodeFetchResponse:
        """
        logger.info("get episodes from WRESTLE UNIVERSE")
        fetched_episodes, fetched_next_page_token = self._episode_fetcher.handle(next_page_token=next_page_token,
                                                        stop_episode_id=stop_episode_id,
                                                        count=3)
        logger.info("fetched_next_page_token: %s", fetched_next_page_token)
        print("fetched_next_page_token: %s", fetched_next_page_token)
        logger.info("translate episodes")
        episodes, casts, video_chapters = EpisodeTranslator.translate(fetched_episodes)

        # 必要に応じて初期化
        self._init_if_needed(dir)

        # すでに存在するjsonファイルに追記する
        with open(f"{dir}/episodes.json", "r") as f:
            episodes += json.load(f)
            # episode_idで重複を削除する
            episodes = list({e["id"]:e for e in episodes}.values())
        with open(f"{dir}/episodes.json", "w") as f:
            json.dump(episodes, f, ensure_ascii=False)

        with open(f"{dir}/casts.json", "r") as f:
            casts += json.load(f)
            # cast_idで重複を削除する
            casts = list({c["id"]:c for c in casts}.values())
        with open(f"{dir}/casts.json", "w") as f:
            json.dump(casts, f, ensure_ascii=False)

        with open(f"{dir}/video_chapters.json", "r") as f:
            video_chapters += json.load(f)
            # video_chapter_idで重複を削除する
            video_chapters = list({v["id"]:v for v in video_chapters}.values())
        with open(f"{dir}/video_chapters.json", "w") as f:
            json.dump(video_chapters, f, ensure_ascii=False)

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

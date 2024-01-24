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

  def handle(self, stop_episode_id: Optional[str] = None, dir: str = DEFAULT_DIR) -> None:
    """WRESTLE UNIVERSEより試合情報を取得する

    Args:
        stop_episode_id (str): 取得を終了する興行ID。この興行が含まれたら取得を終了する
        dir (str): 取得したデータを保存するディレクトリ

    Returns:
        EpisodeFetchResponse:
    """
    logger.info("get episodes from WRESTLE UNIVERSE")
    fetched_episodes = self._episode_fetcher.handle(stop_episode_id)
    logger.info("translate episodes")
    episodes, casts, video_chapters = EpisodeTranslator.translate(fetched_episodes)

    # dirが存在しなければ作成する
    pathlib.Path(dir).mkdir(parents=True, exist_ok=True)

    # それぞれをjsonファイルに保存する
    with open(f"{dir}/episodes.json", "w") as f:
      json.dump(episodes, f, ensure_ascii=False)
    with open(f"{dir}/casts.json", "w") as f:
      json.dump(casts, f, ensure_ascii=False)
    with open(f"{dir}/video_chapters.json", "w") as f:
      json.dump(video_chapters, f, ensure_ascii=False)



if __name__ == "__main__":
    # python -m usecase.pull_episode
    pull_episode = PullEpisodesUsecase()
    pull_episode.handle()

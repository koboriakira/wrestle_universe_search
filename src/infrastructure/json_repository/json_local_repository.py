import pathlib
import json
from domain.infrastructure.json_repository import JsonRepository

DEFAULT_DIR = "data"
EPISODE_JSON = "episodes.json"
CASTS_JSON = "casts.json"
VIDEO_CHAPTERS_JSON = "video_chapters.json"


class JsonLocalRepository(JsonRepository):
    def save_episodes(self, data: list[dict]) -> None:
        self._save(data, EPISODE_JSON)

    def load_episodes(self) -> list[dict]:
        pass

    def save_casts(self, data: list[dict]) -> None:
        self._save(data, CASTS_JSON)

    def load_casts(self) -> list[dict]:
        pass

    def save_video_chapters(self, data: list[dict]) -> None:
        self._save(data, VIDEO_CHAPTERS_JSON)

    def load_video_chapters(self) -> list[dict]:
        pass

    def _save(self, data: list[dict], file_name: str) -> None:
        # ディレクトリが存在しなければ作成する
        dir = DEFAULT_DIR
        pathlib.Path(dir).mkdir(exist_ok=True)

        # ファイルが存在しなければ作成する
        if not pathlib.Path(f"{dir}/{file_name}").exists():
            with open(f"{dir}/{file_name}", "w") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

        # すでに存在するjsonファイルに追記する
        with open(f"{dir}/{file_name}", "r") as f:
            original_data = json.load(f)
            original_data += data
            # episode_idで重複を削除する
            original_data = list({e["id"]:e for e in original_data}.values())
        with open(f"{dir}/{file_name}", "w") as f:
            json.dump(original_data, f, ensure_ascii=False, indent=2)

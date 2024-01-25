import pathlib
import json
from datetime import date as Date
from typing import Optional
from domain.infrastructure.json_repository import JsonRepository

DEFAULT_DIR = "data"
EPISODE_JSON = "episodes.json"
CASTS_JSON = "casts.json"
VIDEO_CHAPTERS_JSON = "video_chapters.json"
EVENTS_JSON = "events.json"

class JsonLocalRepository(JsonRepository):
    def save_episodes(self, data: list[dict]) -> None:
        self._save(data, EPISODE_JSON)

    def load_episodes(self) -> list[dict]:
        with open(f"{DEFAULT_DIR}/{EPISODE_JSON}", "r") as f:
            return json.load(f)

    def save_casts(self, data: list[dict]) -> None:
        self._save(data, CASTS_JSON)

    def load_casts(self, sub_display_name: Optional[str] = None) -> list[dict]:
        casts_json_data = self._load(CASTS_JSON)
        if sub_display_name:
            casts_json_data = [cast for cast in casts_json_data if cast["subDisplayName"] == sub_display_name]
        return casts_json_data

    def save_video_chapters(self, data: list[dict]) -> None:
        self._save(data, VIDEO_CHAPTERS_JSON)

    def load_video_chapters(self, start: Optional[Date] = None, end: Optional[Date] = None) -> list[dict]:
        video_chapters_json_data = self._load(VIDEO_CHAPTERS_JSON)
        if start:
            video_chapters_json_data = [video_chapter for video_chapter in video_chapters_json_data if Date.fromisoformat(video_chapter["matchDate"]) >= start]
        if end:
            video_chapters_json_data = [video_chapter for video_chapter in video_chapters_json_data if Date.fromisoformat(video_chapter["matchDate"]) <= end]
        return video_chapters_json_data

    def save_events(self, data: list[dict]) -> None:
        self._save(data, EVENTS_JSON)

    def load_events(self) -> list[dict]:
        return self._load(EVENTS_JSON)

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

    def _load(self, file_name: str) -> list[dict]:
        with open(f"{DEFAULT_DIR}/{file_name}", "r") as f:
            return json.load(f)

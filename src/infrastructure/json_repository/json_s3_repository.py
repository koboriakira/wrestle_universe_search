import boto3
from botocore.exceptions import NoCredentialsError
import json
from datetime import date as Date
from typing import Optional
from domain.infrastructure.json_repository import JsonRepository
from util.custom_logging import get_logger

logger = get_logger(__name__)

BUCKET_NAME = "wrestler-universe-search-koboriakira"

DIR = "/tmp/"
EPISODE_JSON = "episodes.json"
CASTS_JSON = "casts.json"
VIDEO_CHAPTERS_JSON = "video_chapters.json"
EVENTS_JSON = "events.json"

class JsonLocalRepository(JsonRepository):
    def __init__(self) -> None:
        self.s3_client = boto3.client('s3')

    def save_episodes(self, data: list[dict]) -> None:
        self._save(data, EPISODE_JSON)

    def load_episodes(self) -> list[dict]:
        return self._load(EPISODE_JSON)

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
        # NOTE: ファイルはすでに存在するものとする。そのため初期化するときは手動でS3にファイルをアップロードする必要がある
        try:
            # すでに存在するjsonファイルに追記する
            original_data = self._load(file_name)
            original_data += data

            # idで重複を削除する
            original_data = list({e["id"]:e for e in original_data}.values())

            # ファイルを出力してS3にアップロード
            with open(f"{DIR}/{file_name}", "w") as f:
                json.dump(original_data, f, ensure_ascii=False, indent=2)
            self.s3_client.upload_file(f"{DIR}/{file_name}", BUCKET_NAME, file_name)
        except FileNotFoundError:
            logger.error("ファイルが見つかりませんでした。")
            raise e
        except NoCredentialsError:
            logger.error("認証情報が不足しています。")
            raise e
        except Exception as e:
            logger.error(e)
            raise e

    def _load(self, file_name: str) -> list[dict]:
        filepath = f"{DIR}/{file_name}"
        self.s3_client.download_file(BUCKET_NAME, file_name, filepath)
        with open(filepath, "r") as f:
            return json.load(f)

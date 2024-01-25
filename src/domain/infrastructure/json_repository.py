from abc import ABCMeta, abstractmethod
from typing import Optional
from datetime import date as Date
class JsonRepository(metaclass=ABCMeta):
    @abstractmethod
    def save_episodes(self, data: list[dict]) -> None:
        pass

    @abstractmethod
    def load_episodes(self) -> list[dict]:
        pass

    @abstractmethod
    def save_casts(self, data: list[dict]) -> None:
        pass

    @abstractmethod
    def load_casts(self, sub_display_name: Optional[str] = None) -> list[dict]:
        pass

    @abstractmethod
    def save_video_chapters(self, data: list[dict]) -> None:
        pass

    @abstractmethod
    def load_video_chapters(self, start: Optional[Date] = None, end: Optional[Date] = None) -> list[dict]:
        pass

    @abstractmethod
    def save_events(self, data: list[dict]) -> None:
        pass

    @abstractmethod
    def load_events(self) -> list[dict]:
        pass

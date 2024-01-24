from abc import ABCMeta, abstractmethod

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
    def load_casts(self) -> list[dict]:
        pass

    @abstractmethod
    def save_video_chapters(self, data: list[dict]) -> None:
        pass

    @abstractmethod
    def load_video_chapters(self) -> list[dict]:
        pass
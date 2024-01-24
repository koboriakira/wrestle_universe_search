from dataclasses import dataclass
from domain.match_kind import MatchKind

@dataclass(frozen=True)
class Match:
    order: int
    title: str
    wrestlers: list[str]

    def get_match_kind(self) -> MatchKind:
        return MatchKind.from_title(self.title)

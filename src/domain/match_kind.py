from enum import IntEnum


class MatchKind(IntEnum):
    ALL = 0
    TITLEMATCH = 1
    NORMAL = 2
    NOTMATCH = 3
    SPECIALMATCH = 4
    OFFICIALMATCH = 5
    UNCLASSIFIABLE = 9

    def from_title(title: str) -> "MatchKind":
        match title:
            case "オープニング":
                return MatchKind.NOTMATCH
            case "アップアップガールズ（プロレス）LIVE":
                return MatchKind.NOTMATCH
            case "シングルマッチ":
                return MatchKind.NORMAL
            case "3WAYマッチ":
                return MatchKind.NORMAL
            case "タッグマッチ":
                return MatchKind.NORMAL
            case "オープニングマッチ":
                return MatchKind.NORMAL
            case "6人タッグマッチ":
                return MatchKind.NORMAL
            case "8人タッグマッチ":
                return MatchKind.NORMAL
            case "全力スレッジハンマー":
                return MatchKind.NOTMATCH
            case "インターナショナル・プリンセス選手権試合":
                return MatchKind.TITLEMATCH
            case "インターナショナル・プリンセス王座次期挑戦者決定戦":
                return MatchKind.OFFICIALMATCH
            case "プリンセスタッグ選手権試合":
                return MatchKind.TITLEMATCH
            case "プリンセス・オブ・プリンセス選手権試合":
                return MatchKind.TITLEMATCH
            case "プロレスリングEVE選手権試合":
                return MatchKind.TITLEMATCH
            case "トーナメント決勝戦":
                return MatchKind.OFFICIALMATCH
            case "トーナメント準決勝":
                return MatchKind.OFFICIALMATCH
            case "トーナメント準々決勝":
                return MatchKind.OFFICIALMATCH
            case "トーナメント1回戦":
                return MatchKind.OFFICIALMATCH
            case "トーナメント2回戦":
                return MatchKind.OFFICIALMATCH
            case _:
                return MatchKind.SPECIALMATCH

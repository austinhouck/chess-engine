from enum import Enum


class PlayerColor(str, Enum):
    WHITE = "white"
    BLACK = "black"


class GameStatus(str, Enum):
    """PENDING is a settings-only placeholder, not a real game yet - it's what
    /game/settings creates/updates when the latest game has already started,
    so a settings change never shadows an in-progress game. Every other value
    is persisted the moment it happens, since none of them (a resignation, a
    game abandoned by starting a new one) can be recovered by replaying moves
    alone."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    DRAW = "draw"
    RESIGNED = "resigned"
    ABANDONED = "abandoned"

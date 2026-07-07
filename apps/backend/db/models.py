import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from common.enums import GameStatus, PlayerColor
from db.session import Base
from engine.evaluation import EvalFunction
from engine.search import SearchAlgorithm


class Game(Base):
    """A single game, including the settings it was started with.

    session_id groups games from the same browser session; the most recent
    row for a session is both "the current game" and the source of settings
    for the next POST /game.
    """

    __tablename__ = "games"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    player_color: Mapped[PlayerColor] = mapped_column(default=PlayerColor.WHITE)
    player_name: Mapped[str | None] = mapped_column(default=None)
    computer_max_depth: Mapped[int] = mapped_column(default=4)
    computer_algorithm: Mapped[SearchAlgorithm] = mapped_column(default=SearchAlgorithm.NAIVE_MINIMAX)
    computer_evaluator: Mapped[EvalFunction] = mapped_column(default=EvalFunction.SHANNON)
    status: Mapped[GameStatus] = mapped_column(default=GameStatus.PENDING)
    moves: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    time_started: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    time_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=lambda: datetime.now(UTC)
    )

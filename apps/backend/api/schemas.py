import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from common.enums import GameStatus, PlayerColor
from engine.evaluation import EvalFunction
from engine.search import SearchAlgorithm

ExportFormat = Literal["pgn", "fen"]


class SettingsIn(BaseModel):
    player_color: PlayerColor | None = None
    player_name: str | None = None
    computer_max_depth: int | None = None
    computer_algorithm: SearchAlgorithm | None = None
    computer_evaluator: EvalFunction | None = None


class SettingsOut(BaseModel):
    player_color: PlayerColor
    player_name: str | None
    computer_max_depth: int
    computer_algorithm: SearchAlgorithm
    computer_evaluator: EvalFunction


class MoveIn(BaseModel):
    move: str


class GameOut(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    player_color: PlayerColor
    player_name: str | None
    computer_max_depth: int
    computer_algorithm: SearchAlgorithm
    computer_evaluator: EvalFunction
    moves: list[str]
    fen: str
    turn: PlayerColor
    status: GameStatus
    result: str
    time_started: datetime
    time_updated: datetime

import uuid
from datetime import date

from bulletchess import WHITE, Board, Move
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import engine
from api.schemas import GameOut
from common.enums import GameStatus, PlayerColor
from common.errors import GameOverError
from db.models import Game
from engine.evaluation import EvalFunction
from engine.search import SearchAlgorithm


def _default_settings() -> dict:
    return {
        "player_color": PlayerColor.WHITE,
        "player_name": None,
        "computer_max_depth": 4,
        "computer_algorithm": SearchAlgorithm.NAIVE_MINIMAX,
        "computer_evaluator": EvalFunction.SHANNON,
    }


async def get_latest_game(db: AsyncSession, session_id: uuid.UUID) -> Game | None:
    """The most recent row for this session, including a trailing PENDING
    settings placeholder if one exists. Use get_latest_started_game for
    anything that should ignore that placeholder."""
    result = await db.execute(
        select(Game).where(Game.session_id == session_id).order_by(Game.time_started.desc()).limit(1)
    )
    return result.scalar_one_or_none()


async def get_latest_started_game(db: AsyncSession, session_id: uuid.UUID) -> Game | None:
    """The session's actual current game: the most recent row that was
    started via POST /game, skipping any trailing PENDING settings
    placeholder created by /game/settings."""
    result = await db.execute(
        select(Game)
        .where(Game.session_id == session_id, Game.status != GameStatus.PENDING)
        .order_by(Game.time_started.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def get_settings(db: AsyncSession, session_id: uuid.UUID | None) -> dict:
    """Settings that the next POST /game (or /game/settings update) would start from."""
    if session_id is None:
        return _default_settings()
    latest = await get_latest_game(db, session_id)
    if latest is None:
        return _default_settings()
    return {
        "player_color": latest.player_color,
        "player_name": latest.player_name,
        "computer_max_depth": latest.computer_max_depth,
        "computer_algorithm": latest.computer_algorithm,
        "computer_evaluator": latest.computer_evaluator,
    }


async def get_or_create_pending_game(db: AsyncSession, session_id: uuid.UUID) -> Game:
    """The session's PENDING settings placeholder, creating one if needed.

    Settings are inherited from the most recent game, if any. An existing
    PENDING row is always reused rather than duplicated, so this is safe to
    call repeatedly before POST /game is next called.
    """
    latest = await get_latest_game(db, session_id)
    if latest is not None and latest.status == GameStatus.PENDING:
        return latest

    settings = {
        "player_color": latest.player_color,
        "player_name": latest.player_name,
        "computer_max_depth": latest.computer_max_depth,
        "computer_algorithm": latest.computer_algorithm,
        "computer_evaluator": latest.computer_evaluator,
    } if latest is not None else _default_settings()

    game = Game(session_id=session_id, moves=[], **settings)
    db.add(game)
    await db.flush()
    return game


async def update_settings(db: AsyncSession, session_id: uuid.UUID, **fields) -> Game:
    """`fields` should only contain keys the caller explicitly wants to change
    (e.g. via `SettingsIn.model_dump(exclude_unset=True)`), since a value of
    None is a valid, deliberate way to clear player_name."""
    game = await get_or_create_pending_game(db, session_id)
    for key, value in fields.items():
        setattr(game, key, value)
    await db.flush()
    return game


def board_from_moves(moves: list[str]) -> Board:
    """Reconstruct the board by replaying stored UCI moves from the start.
    board.history ends up identical to a live-played game's, so the shared
    engine.export_pgn/export_fen work on it unchanged."""
    board = Board()
    for uci in moves:
        board.apply(Move.from_uci(uci))
    return board


def _apply_computer_move_if_due(game: Game, board: Board) -> None:
    """Mutates game.moves and board in place if it's the computer's turn."""
    if engine.is_computers_turn(board, game.player_color):
        outcome = engine.compute_best_move(board, game.computer_algorithm, game.computer_evaluator, game.computer_max_depth)
        board.apply(outcome.move)
        game.moves = [*game.moves, outcome.move.uci()]


async def apply_player_move(db: AsyncSession, game: Game, move_str: str) -> Game:
    if game.status != GameStatus.IN_PROGRESS:
        raise GameOverError("This game has already ended.")

    board = board_from_moves(game.moves)
    move = engine.parse_move(move_str, board)
    board.apply(move)
    game.moves = [*game.moves, move.uci()]

    terminal = engine.terminal_status(board)
    if terminal is not None:
        game.status = terminal
    else:
        _apply_computer_move_if_due(game, board)
        terminal = engine.terminal_status(board)
        if terminal is not None:
            game.status = terminal

    await db.flush()
    return game


async def resign_game(db: AsyncSession, game: Game) -> Game:
    if game.status != GameStatus.IN_PROGRESS:
        raise GameOverError("Game is not in progress.")
    game.status = GameStatus.RESIGNED
    await db.flush()
    return game


async def start_new_game(db: AsyncSession, session_id: uuid.UUID) -> Game:
    """Start a new game from the session's current settings.

    If a previous game was still in progress, it's marked ABANDONED - it
    stays in the database, just no longer the session's current game.
    """
    previous = await get_latest_started_game(db, session_id)
    if previous is not None and previous.status == GameStatus.IN_PROGRESS:
        previous.status = GameStatus.ABANDONED

    game = await get_or_create_pending_game(db, session_id)
    game.status = GameStatus.IN_PROGRESS

    board = board_from_moves(game.moves)
    _apply_computer_move_if_due(game, board)
    terminal = engine.terminal_status(board)
    if terminal is not None:
        game.status = terminal

    await db.flush()
    return game


def _pgn_result(game: Game, board: Board) -> str:
    if game.status == GameStatus.RESIGNED:
        # Only the human can resign via the API, so resigning is always a loss for them.
        return "0-1" if game.player_color == PlayerColor.WHITE else "1-0"
    return engine.pgn_result(board)


def to_fen(game: Game) -> str:
    return engine.export_fen(board_from_moves(game.moves))


def to_pgn(game: Game) -> str:
    board = board_from_moves(game.moves)
    white_name = game.player_name if game.player_color == PlayerColor.WHITE else "Engine"
    black_name = game.player_name if game.player_color == PlayerColor.BLACK else "Engine"
    return engine.export_pgn(
        board,
        white=white_name or "Human",
        black=black_name or "Engine",
        game_date=game.time_started.date() if game.time_started else date.today(),
        result=_pgn_result(game, board),
    )


def build_game_out(game: Game) -> GameOut:
    board = board_from_moves(game.moves)
    turn = PlayerColor.WHITE if board.turn == WHITE else PlayerColor.BLACK
    return GameOut(
        id=game.id,
        session_id=game.session_id,
        player_color=game.player_color,
        player_name=game.player_name,
        computer_max_depth=game.computer_max_depth,
        computer_algorithm=game.computer_algorithm,
        computer_evaluator=game.computer_evaluator,
        moves=game.moves,
        fen=board.fen(),
        turn=turn,
        status=game.status,
        result=_pgn_result(game, board),
        time_started=game.time_started,
        time_updated=game.time_updated,
    )

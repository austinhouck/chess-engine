import uuid

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from api import game_service
from api.schemas import ExportFormat, GameOut, MoveIn, SettingsIn, SettingsOut
from common.config import settings
from common.errors import GameOverError, InvalidMoveError
from db import get_db

SESSION_COOKIE_NAME = "session_id"
SESSION_COOKIE_MAX_AGE = 60 * 60 * 24 * 30  # 30 days

app = FastAPI(title="Chess Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_session_id(request: Request) -> uuid.UUID | None:
    raw = request.cookies.get(SESSION_COOKIE_NAME)
    if raw is None:
        return None
    try:
        return uuid.UUID(raw)
    except ValueError:
        return None


def require_session_id(request: Request) -> uuid.UUID:
    session_id = get_session_id(request)
    if session_id is None:
        raise HTTPException(status_code=404, detail="No active session. Start a game with POST /game.")
    return session_id


def set_session_cookie(response: Response, session_id: uuid.UUID) -> None:
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=str(session_id),
        httponly=True,
        samesite="lax",
        max_age=SESSION_COOKIE_MAX_AGE,
    )


async def get_or_start_session_id(request: Request, response: Response) -> uuid.UUID:
    """Session id for write endpoints that may bootstrap a brand new session."""
    session_id = get_session_id(request)
    if session_id is None:
        session_id = uuid.uuid4()
        set_session_cookie(response, session_id)
    return session_id


@app.post("/game", response_model=GameOut)
async def start_game(
    session_id: uuid.UUID = Depends(get_or_start_session_id),
    db: AsyncSession = Depends(get_db),
) -> GameOut:
    game = await game_service.start_new_game(db, session_id)
    await db.commit()
    return game_service.build_game_out(game)


@app.get("/game", response_model=GameOut)
async def read_game(
    session_id: uuid.UUID = Depends(require_session_id),
    db: AsyncSession = Depends(get_db),
) -> GameOut:
    game = await game_service.get_latest_started_game(db, session_id)
    if game is None:
        raise HTTPException(status_code=404, detail="No game found for this session. Start one with POST /game.")
    return game_service.build_game_out(game)


@app.get("/game/settings", response_model=SettingsOut)
async def read_settings(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> SettingsOut:
    session_id = get_session_id(request)
    return SettingsOut(**await game_service.get_settings(db, session_id))


@app.post("/game/settings", response_model=SettingsOut)
async def write_settings(
    payload: SettingsIn,
    session_id: uuid.UUID = Depends(get_or_start_session_id),
    db: AsyncSession = Depends(get_db),
) -> SettingsOut:
    game = await game_service.update_settings(db, session_id, **payload.model_dump(exclude_unset=True))
    await db.commit()
    return SettingsOut(
        player_color=game.player_color,
        player_name=game.player_name,
        computer_max_depth=game.computer_max_depth,
        computer_algorithm=game.computer_algorithm,
        computer_evaluator=game.computer_evaluator,
    )


@app.post("/game/move", response_model=GameOut)
async def make_move(
    payload: MoveIn,
    session_id: uuid.UUID = Depends(require_session_id),
    db: AsyncSession = Depends(get_db),
) -> GameOut:
    game = await game_service.get_latest_started_game(db, session_id)
    if game is None:
        raise HTTPException(status_code=404, detail="No game found for this session. Start one with POST /game.")
    try:
        game = await game_service.apply_player_move(db, game, payload.move)
    except (InvalidMoveError, GameOverError) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    await db.commit()
    return game_service.build_game_out(game)


@app.post("/game/resign", response_model=GameOut)
async def resign(
    session_id: uuid.UUID = Depends(require_session_id),
    db: AsyncSession = Depends(get_db),
) -> GameOut:
    game = await game_service.get_latest_started_game(db, session_id)
    if game is None:
        raise HTTPException(status_code=404, detail="No game found for this session. Start one with POST /game.")
    try:
        game = await game_service.resign_game(db, game)
    except GameOverError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    await db.commit()
    return game_service.build_game_out(game)


@app.get("/game/export")
async def export_game(
    format: ExportFormat,
    session_id: uuid.UUID = Depends(require_session_id),
    db: AsyncSession = Depends(get_db),
) -> Response:
    game = await game_service.get_latest_started_game(db, session_id)
    if game is None:
        raise HTTPException(status_code=404, detail="No game found for this session. Start one with POST /game.")

    if format == "pgn":
        content, filename = game_service.to_pgn(game), "game.pgn"
    else:
        content, filename = game_service.to_fen(game), "game.fen"

    return Response(
        content=content,
        media_type="text/plain",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

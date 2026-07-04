# Chess Engine Backend

The chess engine (`engine/`), an interactive CLI built on it (`cli/`), and a
FastAPI + Postgres API (`api/`, `db/`) that exposes it over HTTP. Shared
vocabulary/config used by more than one of those (`enums`, `errors`,
`config`) lives in `common/`. See the repo root README for overall
requirements and setup.

## CLI

```
cd apps/backend
uv run python -m cli.main
```

(equivalent to `./bin/run.sh` from the repo root)

Also available at any time inside the shell via `help` or `help <command>`.

| Command | Description |
| --- | --- |
| `set_params` | Interactively configure search depth, opponent type, and verbose output. |
| `set_opponent [human\|computer]` | Set the opponent type. |
| `move [move]` | Make a move on the board (SAN or UCI). |
| `show_board` | Show the current chess board. |
| `legal_moves` | List legal moves for the current board state. |
| `get_evaluation [depth]` | Evaluate the board using the minimax algorithm. |
| `export [pgn\|fen] [filename]` | Export the current game as PGN or the current position as FEN. Prints to stdout if no filename is given. |
| `reset_board` | Reset the board to the initial state. |
| `clear` | Clear the console screen. |
| `exit` | Exit the application. |

## API Server

The API (`api/app.py`) is a FastAPI app backed by Postgres.

Start Postgres (from the repo root):

```
docker compose up -d
```

Apply migrations, then run the server (from `apps/backend`):

```
uv run alembic -c db/alembic.ini upgrade head
uv run uvicorn api.app:app --reload --port 8000
```

By default it connects to the Postgres container using the credentials in
`docker-compose.yml` (`postgresql+asyncpg://chess:chess@localhost:5432/chess`).
Override this by setting `DATABASE_URL` in an `.env` file in `apps/backend/`
(see `common/config.py`).

A browser session is tracked with an httponly `session_id` cookie, set the
first time `POST /game` or `POST /game/settings` is called. All endpoints
below operate on that session.

| Endpoint | Description |
| --- | --- |
| `POST /game` | Start a new game using the session's current settings (see `/game/settings`). If `player_color` is `black`, the computer immediately plays White's opening move. If a previous game was still in progress, it's marked `abandoned`. |
| `GET /game` | Get the session's current game: moves, FEN, whose turn it is, and status. |
| `GET /game/settings` | Get the settings that the next `POST /game` will use (`player_color`, `player_name`, `computer_max_depth`, `computer_algorithm`, `computer_evaluator`). Returns hardcoded defaults if the session has no games yet. |
| `POST /game/settings` | Update those settings. Only affects a game that hasn't started yet — it has no effect on a game already in progress. |
| `POST /game/move` | Submit a move (SAN or UCI). Validates it's legal, applies it, then applies the computer's reply if it's now the computer's turn. 400s if the game has already ended. |
| `POST /game/resign` | Concede the current game (marks it `resigned`; the opponent is recorded as the winner). 400s if the game isn't in progress. |
| `GET /game/export?format=pgn\|fen` | Download the current game as a PGN or FEN file. |

`status` is one of: `pending` (a settings-only placeholder, never returned by
`GET /game`), `in_progress`, `checkmate`, `stalemate`, `draw`, `resigned`, or
`abandoned` (superseded by a new game before it ended).

## Database

There's a single `games` table (see `db/models.py`); there is no separate
sessions table. Columns:

| Column | Description |
| --- | --- |
| `id` | Primary key (UUID) for this game. |
| `session_id` | Groups games from the same browser session. Not a foreign key — just an opaque UUID tag from the `session_id` cookie. |
| `player_color` | `white` or `black` — which side the human is playing. |
| `player_name` | Human player's display name (nullable). |
| `computer_max_depth` | Search depth (plies) for the computer's moves. |
| `computer_algorithm` | Which `engine.search.SearchAlgorithm` the computer uses - stored/returned as its string value (e.g. `"naive_minimax"`); each member also carries the actual `Search` implementation class, so this is the only enum for this choice. |
| `computer_evaluator` | Which `engine.evaluation.EvalFunction` the computer uses, same single-enum pattern as `computer_algorithm`. |
| `status` | `pending`/`in_progress`/`checkmate`/`stalemate`/`draw`/`resigned`/`abandoned`. See below — this is the one piece of game state that can't be recomputed from `moves`. |
| `moves` | Ordered array of UCI move strings played so far. This is the source of truth for board state — FEN and whose turn it is are recomputed on the fly by replaying these moves through a `bulletchess.Board` (see `api/game_service.py`'s `board_from_moves`), rather than stored redundantly. |
| `time_started` / `time_updated` | Timestamps (`timestamptz`). |

**Why `status` is persisted rather than computed:** FEN and turn can always be
derived by replaying `moves`, but *why a game ended* can't be — a resignation
or an abandoned game leaves the board in an otherwise-ordinary, non-terminal
position. So `status` is written once, at the moment it happens:

- A fresh row starts as `pending` — this is a settings-only placeholder (see
  below), not a real game yet.
- `POST /game` flips it to `in_progress`.
- `POST /game/move` sets it to `checkmate`/`stalemate`/`draw` if the resulting
  position is terminal; otherwise it stays `in_progress`.
- `POST /game/resign` sets it to `resigned`.
- `POST /game` also sets the *previous* game to `abandoned` if it was still
  `in_progress` when the new one started — it isn't deleted, just no longer
  current.

Only `pending` and `in_progress` accept further moves/settings changes;
everything else is a terminal state.

**"Current game" resolution**, since there's no separate sessions table:
`GET /game`, `POST /game/move`, `POST /game/resign`, and `/game/export` all
use the most recent `games` row for the session with `status != pending`
(`api/game_service.py`'s `get_latest_started_game`). `POST /game/settings`
instead reuses or creates a trailing `pending` row
(`get_or_create_pending_game`) — this is what keeps a settings change from
ever shadowing a real in-progress game in `GET /game`.

Migrations live in `db/alembic/`. After changing `db/models.py`, from
`apps/backend`:

```
uv run alembic -c db/alembic.ini revision --autogenerate -m "describe the change"
uv run alembic -c db/alembic.ini upgrade head
```

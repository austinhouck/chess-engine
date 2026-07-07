"""The chess engine: move validation, computer search, and PGN/FEN export
(engine.core), backed by the search algorithms (engine.search) and
evaluators (engine.evaluation) it picks between.

This re-exports engine.core's public functions so callers can keep writing
`import engine` / `from engine import Engine, ...` without caring that the
implementation lives in the core submodule.
"""

from engine.core import (
    Engine,
    SearchOutcome,
    compute_best_move,
    export_fen,
    export_pgn,
    is_computers_turn,
    parse_move,
    pgn_result,
    terminal_status,
)

__all__ = [
    "Engine",
    "SearchOutcome",
    "compute_best_move",
    "export_fen",
    "export_pgn",
    "is_computers_turn",
    "parse_move",
    "pgn_result",
    "terminal_status",
]

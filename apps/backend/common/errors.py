"""Errors shared across the engine, db, and api layers."""


class InvalidMoveError(ValueError):
    """Raised by engine.parse_move: the move is malformed or illegal for the current board."""


class GameOverError(ValueError):
    """Raised by api/game_service.py: the game can't accept a move/resignation because it's already over."""

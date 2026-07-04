from datetime import date

import pytest
from bulletchess import Board, Move

from common.enums import GameStatus, PlayerColor
from common.errors import InvalidMoveError
from engine.core import (
    Engine,
    compute_best_move,
    export_fen,
    export_pgn,
    is_computers_turn,
    parse_move,
    pgn_result,
    terminal_status,
)
from engine.evaluation import EvalFunction
from engine.search import SearchAlgorithm

FOOLS_MATE_MOVES = ["f2f3", "e7e5", "g2g4", "d8h4"]  # Black delivers Qh4#


def _play(*ucis: str) -> Board:
    board = Board()
    for uci in ucis:
        board.apply(Move.from_uci(uci))
    return board


def test_parse_move_accepts_san():
    move = parse_move("e4", Board())
    assert move.uci() == "e2e4"


def test_parse_move_accepts_uci():
    move = parse_move("e2e4", Board())
    assert move.uci() == "e2e4"


def test_parse_move_rejects_an_illegal_move():
    with pytest.raises(InvalidMoveError):
        parse_move("e5", Board())  # black's move, but white is to play


def test_parse_move_rejects_garbage_input():
    with pytest.raises(InvalidMoveError):
        parse_move("not-a-move", Board())


def test_terminal_status_is_none_for_the_starting_position():
    assert terminal_status(Board()) is None


def test_terminal_status_detects_checkmate():
    assert terminal_status(_play(*FOOLS_MATE_MOVES)) == GameStatus.CHECKMATE


def test_pgn_result_is_a_placeholder_for_an_ongoing_game():
    assert pgn_result(Board()) == "*"


def test_pgn_result_reflects_the_checkmate_winner():
    assert pgn_result(_play(*FOOLS_MATE_MOVES)) == "0-1"  # black mated white


@pytest.mark.parametrize(
    ("player_color", "expected"),
    [
        (PlayerColor.WHITE, False),  # white to move, human plays white -> human's turn
        (PlayerColor.BLACK, True),  # white to move, human plays black -> computer's turn
    ],
)
def test_is_computers_turn(player_color, expected):
    assert is_computers_turn(Board(), player_color) is expected


def test_compute_best_move_returns_a_legal_move():
    board = Board()
    outcome = compute_best_move(board, SearchAlgorithm.NAIVE_MINIMAX, EvalFunction.SHANNON, depth=1)
    assert outcome.move in board.legal_moves()


def test_compute_best_move_rejects_depth_zero():
    """Depth 0 means "evaluate this leaf, don't search" - there's no move to return."""
    with pytest.raises(ValueError):
        compute_best_move(Board(), SearchAlgorithm.NAIVE_MINIMAX, EvalFunction.SHANNON, depth=0)


def test_export_fen_matches_the_board():
    assert export_fen(Board()) == Board().fen()


def test_export_pgn_includes_headers_moves_and_result_override():
    board = _play("e2e4")
    pgn = export_pgn(board, white="Alice", black="Bob", game_date=date(2024, 1, 1), result="1-0")
    assert '[White "Alice"]' in pgn
    assert '[Black "Bob"]' in pgn
    assert '[Result "1-0"]' in pgn
    assert "1. e4" in pgn


class TestEngine:
    def test_make_move_applies_a_legal_move(self):
        engine = Engine()
        engine.auto_respond = False
        assert engine.make_move("e4") is True
        assert engine.board.fen() == _play("e2e4").fen()

    def test_make_move_rejects_an_illegal_move(self):
        engine = Engine()
        assert engine.make_move("e5") is False
        assert engine.board.fen() == Board().fen()

    def test_auto_respond_triggers_a_computer_reply(self):
        engine = Engine()
        engine.depth = 1
        engine.make_move("e4")
        assert len(engine.board.history) == 2  # white's move, then the computer's reply

    def test_reset_board_returns_to_the_starting_position(self):
        engine = Engine()
        engine.make_move("e4")
        engine.reset_board()
        assert engine.board.fen() == Board().fen()

    def test_export_fen_and_pgn_delegate_to_the_current_board(self):
        engine = Engine()
        engine.auto_respond = False
        engine.make_move("e4")
        assert engine.export_fen() == engine.board.fen()
        assert "1. e4" in engine.export_pgn()

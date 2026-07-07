"""Chess-domain operations shared by the CLI (cli/main.py) and the API
(api/game_service.py): parsing/validating a move, picking the computer's
move, and PGN/FEN export. Everything here operates on a bulletchess.Board and
has no notion of persistence or sessions - that live-vs-replayed distinction
is invisible to these functions since board.history is populated identically
either way (see api/game_service.py's board_from_moves)."""

import time
from datetime import date
from typing import NamedTuple

from bulletchess import (
    CHECKMATE,
    DRAW,
    FIFTY_MOVE_TIMEOUT,
    FORCED_DRAW,
    INSUFFICIENT_MATERIAL,
    STALEMATE,
    THREEFOLD_REPETITION,
    WHITE,
    Board,
    Move,
)

from common.enums import GameStatus, PlayerColor
from common.errors import InvalidMoveError
from engine.evaluation import EvalFunction
from engine.search import Search, SearchAlgorithm


def parse_move(move_str: str, board: Board) -> Move:
    """Parse a move in SAN or UCI notation, validating it's legal for `board`."""
    try:
        return Move.from_san(move_str, board)
    except ValueError:
        pass
    try:
        move = Move.from_uci(move_str)
    except ValueError:
        raise InvalidMoveError(f"Invalid move format: {move_str}. Use SAN or UCI format.") from None
    if move not in board.legal_moves():
        raise InvalidMoveError(f"Illegal move: {move_str}")
    return move


def terminal_status(board: Board) -> GameStatus | None:
    """The status forced by `board` itself, or None if the game could still continue.

    Can't detect a resignation or an abandoned game - those leave no trace on
    the board, so a caller that needs them (game_service) records them separately.
    """
    if board in CHECKMATE:
        return GameStatus.CHECKMATE
    if board in STALEMATE:
        return GameStatus.STALEMATE
    if board in DRAW or board in FORCED_DRAW:
        return GameStatus.DRAW
    return None


def pgn_result(board: Board) -> str:
    """The PGN result tag implied by the board alone ('*' if not visibly over)."""
    status = terminal_status(board)
    if status == GameStatus.CHECKMATE:
        return "0-1" if board.turn == WHITE else "1-0"
    if status in (GameStatus.DRAW, GameStatus.STALEMATE):
        return "1/2-1/2"
    return "*"


def is_computers_turn(board: Board, player_color: PlayerColor) -> bool:
    """Whether it's the opponent's turn, given which color `player_color` is playing."""
    player_is_white = player_color == PlayerColor.WHITE
    return player_is_white != (board.turn == WHITE)


class SearchOutcome(NamedTuple):
    move: Move
    evaluation: float
    search: Search


def compute_best_move(board: Board, algorithm: SearchAlgorithm, evaluator: EvalFunction, depth: int) -> SearchOutcome:
    """The best move for whoever's turn it is on `board`.

    The evaluator scores a position from White's perspective, so whoever is
    on the move must maximize that score if they're White, minimize it if
    they're Black - this can't be a fixed value.
    """
    maximizing_player = board.turn == WHITE
    search = algorithm.search_class(evaluator.eval_class())
    move, evaluation = search.search(board, depth, maximizing_player)
    if move is None:
        raise ValueError("No move found: is the game already over, or was depth 0?")
    return SearchOutcome(move, evaluation, search)


def export_fen(board: Board) -> str:
    return board.fen()


def export_pgn(
    board: Board,
    *,
    white: str,
    black: str,
    game_date: date,
    result: str | None = None,
    event: str = "Casual Game",
) -> str:
    """PGN text for `board`'s move history (board.history).

    `result` overrides the board-derived result tag - needed for a
    resignation, which isn't visible on the board itself.
    """
    replay = Board()
    sans: list[str] = []
    for move in board.history:
        sans.append(move.san(replay))
        replay.apply(move)

    result = result if result is not None else pgn_result(board)
    movetext_parts = [
        f"{i // 2 + 1}. {sans[i]}" + (f" {sans[i + 1]}" if i + 1 < len(sans) else "")
        for i in range(0, len(sans), 2)
    ]
    movetext = " ".join([*movetext_parts, result]) if sans else result

    headers = {
        "Event": event,
        "Site": "?",
        "Date": game_date.strftime("%Y.%m.%d"),
        "Round": "?",
        "White": white,
        "Black": black,
        "Result": result,
    }
    header_lines = [f'[{key} "{value}"]' for key, value in headers.items()]
    return "\n".join(header_lines) + "\n\n" + movetext + "\n"


class Engine:
    """Stateful wrapper around the functions above, for the interactive CLI (main.py)."""

    def __init__(self) -> None:
        self.board: Board = Board()
        self.auto_respond: bool = True  # Automatically respond to moves
        self.depth: int = 4  # Default depth for minimax evaluation
        self.verbose: bool = False  # Verbose output
        self.game_date: date = date.today()  # Date this game began, for PGN export
        self.eval_function: EvalFunction = EvalFunction.SHANNON
        self.search_algorithm: SearchAlgorithm = SearchAlgorithm.NAIVE_MINIMAX

    def get_legal_moves(self) -> list[Move]:
        return self.board.legal_moves()

    def make_move(self, move_str: str) -> bool:
        """Make a move on the board. If auto_respond is True, the engine will make a move in response."""
        move_number: int = self.board.fullmove_number
        try:
            move = parse_move(move_str, self.board)
        except InvalidMoveError as e:
            print(f"Error making move: {e}")
            return False

        self.board.apply(move)
        print(f"Move {move_number}: White plays {move}")
        if not self._log_game_over() and self.auto_respond:
            self.make_computer_move()
        return True

    def make_computer_move(self) -> None:
        if self.auto_respond:
            move_number: int = self.board.fullmove_number
            start = time.perf_counter()
            outcome = compute_best_move(self.board, self.search_algorithm, self.eval_function, self.depth)
            elapsed = time.perf_counter() - start

            self.board.apply(outcome.move)
            print(f"Move {move_number}: Black plays {outcome.move}")

            if self.verbose:
                print(f"  evaluation: {outcome.evaluation}")
                print(f"  search took {elapsed:.2f}s ({outcome.search.eval_time:.2f}s in evaluate)")
                for ply in sorted(outcome.search.node_counts):
                    print(f"    ply {ply}: {outcome.search.node_counts[ply]} nodes")
                print(f"Board after computer move:\n{self.show_board()}")

            self._log_game_over()
        return None

    def reset_board(self) -> None:
        self.board = Board()
        self.game_date = date.today()

    def show_board(self) -> str:
        return str(self.board)

    def export_fen(self) -> str:
        """Export the current position as a FEN string."""
        return export_fen(self.board)

    def export_pgn(self) -> str:
        """Export the current game (since the last reset) as a PGN string."""
        return export_pgn(self.board, white="Human", black="Engine", game_date=self.game_date)

    def _log_game_over(self) -> bool:
        """Print a message if the game has ended. Returns True if it has."""
        board = self.board
        if board in CHECKMATE:
            winner = "Black" if board.turn == WHITE else "White"
            print(f"Checkmate! {winner} wins.")
            return True
        if board in STALEMATE:
            print("Game over: draw by stalemate.")
            return True
        if board in INSUFFICIENT_MATERIAL:
            print("Game over: draw by insufficient material.")
            return True
        if board in FIFTY_MOVE_TIMEOUT:
            print("Game over: draw by fifty-move rule.")
            return True
        if board in THREEFOLD_REPETITION:
            print("Game over: draw by threefold repetition.")
            return True
        if board in DRAW or board in FORCED_DRAW:
            print("Game over: draw.")
            return True
        return False

import time
from datetime import date

from bulletchess import *
from evaluation import EvalFunction
from search import SearchAlgorithm

class Engine:
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
            move: Move | None = Move.from_san(move_str, self.board)  # Validate SAN format
            print(f"Parsed SAN format move: {move}")
        except ValueError:
            try:
                move = Move.from_uci(move_str)  # Validate UCI format
                print(f"Parsed UCI format move: {move}")
            except ValueError:
                raise ValueError(f"Invalid move format: {move_str}. Use SAN or UCI format.")
        except Exception as e:
            raise ValueError(f"Error parsing move: {e}")

        try:
            self.board.apply(move)
            print(f"Move {move_number}: White plays {move}")
            if not self._log_game_over() and self.auto_respond:
                self.make_computer_move()
            return True
        except Exception as e:
            print(f"Error making move: {e}")
            return False

    def make_computer_move(self) -> None:
        if self.auto_respond:
            # Engine is black, so engine is minimizing player
            move_number: int = self.board.fullmove_number
            search = self.search_algorithm.value(self.eval_function.value())
            start = time.perf_counter()
            best_move, eval = search.search(self.board, self.depth, False)
            elapsed = time.perf_counter() - start

            self.board.apply(best_move)
            print(f"Move {move_number}: Black plays {best_move}")

            if self.verbose:
                print(f"  evaluation: {eval}")
                print(f"  search took {elapsed:.2f}s ({search.eval_time:.2f}s in evaluate)")
                for ply in sorted(search.node_counts):
                    print(f"    ply {ply}: {search.node_counts[ply]} nodes")
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
        return self.board.fen()

    def export_pgn(self) -> str:
        """Export the current game (since the last reset) as a PGN string."""
        replay = Board()
        sans: list[str] = []
        for move in self.board.history:
            sans.append(move.san(replay))
            replay.apply(move)

        result = self._pgn_result()
        movetext_parts = [
            f"{i // 2 + 1}. {sans[i]}" + (f" {sans[i + 1]}" if i + 1 < len(sans) else "")
            for i in range(0, len(sans), 2)
        ]
        movetext = " ".join(movetext_parts + [result])

        headers = {
            "Event": "Casual Game",
            "Site": "?",
            "Date": self.game_date.strftime("%Y.%m.%d"),
            "Round": "?",
            "White": "Human",
            "Black": "Engine",
            "Result": result,
        }
        header_lines = [f'[{key} "{value}"]' for key, value in headers.items()]
        return "\n".join(header_lines) + "\n\n" + movetext + "\n"

    def _pgn_result(self) -> str:
        """Return the PGN result tag for the current position: '1-0', '0-1', '1/2-1/2', or '*'."""
        board = self.board
        if board in CHECKMATE:
            return "0-1" if board.turn == WHITE else "1-0"
        if board in DRAW or board in FORCED_DRAW:
            return "1/2-1/2"
        return "*"

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

from abc import ABC, abstractmethod
from enum import Enum

from bulletchess import *
from bulletchess.utils import doubled_pawns, backwards_pawns, isolated_pawns, mobility


class Evaluator(ABC):
    """Interface for a board evaluation function."""

    @abstractmethod
    def evaluate(self, board: Board) -> float:
        """Score a position from White's perspective: positive favors White."""
        ...


class ShannonEvaluator(Evaluator):
    """Claude Shannon's original chess evaluation function: simple material count.
    $f(P)=200(K-K')+9(Q-Q')+5(R-R')+3(B-B'+N-N')+(P-P')-.5(D-D'+S-S'+I-I')+.1(M-M')$

    Shannon, C.E. (1988). Programming a Computer for Playing Chess. In: Levy, D.
    (eds) Computer Chess Compendium. Springer, New York, NY.
    https://doi.org/10.1007/978-1-4757-1968-0_1
    """

    def evaluate(self, board: Board) -> float:
        # Per Shannon's paper, K-K' isn't a literal king count (both sides always
        # have exactly one king on the board in any legal position) - it stands in
        # for whether either side has been checkmated.
        if board in CHECKMATE:
            return -200.0 if board.turn == WHITE else 200.0
        if board in DRAW or board in FORCED_DRAW:
            return 0.0

        # Piece Counts
        white_queens = self._bit_count(board[WHITE, QUEEN])
        black_queens = self._bit_count(board[BLACK, QUEEN])
        white_rooks = self._bit_count(board[WHITE, ROOK])
        black_rooks = self._bit_count(board[BLACK, ROOK])
        white_bishops = self._bit_count(board[WHITE, BISHOP])
        black_bishops = self._bit_count(board[BLACK, BISHOP])
        white_knights = self._bit_count(board[WHITE, KNIGHT])
        black_knights = self._bit_count(board[BLACK, KNIGHT])
        white_pawns = self._bit_count(board[WHITE, PAWN])
        black_pawns = self._bit_count(board[BLACK, PAWN])

        # Doubled, Isolated, and Passed Pawns
        white_doubled_pawns = self._bit_count(doubled_pawns(board, WHITE))
        black_doubled_pawns = self._bit_count(doubled_pawns(board, BLACK))
        white_backwards_pawns = self._bit_count(backwards_pawns(board, WHITE))
        black_backwards_pawns = self._bit_count(backwards_pawns(board, BLACK))
        white_isolated_pawns = self._bit_count(isolated_pawns(board, WHITE))
        black_isolated_pawns = self._bit_count(isolated_pawns(board, BLACK))

        # Net Mobility
        M = mobility(board)

        # Evaluation Score
        score = (9 * (white_queens - black_queens) +
                 5 * (white_rooks - black_rooks) +
                 3 * (white_bishops - black_bishops + white_knights - black_knights) +
                 (white_pawns - black_pawns) -
                 .5 * (white_doubled_pawns - black_doubled_pawns) -
                 .5 * (white_backwards_pawns - black_backwards_pawns) -
                 .5 * (white_isolated_pawns - black_isolated_pawns) +
                 .1 * M
        )

        return score

    @staticmethod
    def _bit_count(bitboard: Bitboard) -> int:
        return bin(int(bitboard)).count('1')


class EvalFunction(Enum):
    """Selects which Evaluator class Search uses to score a board."""
    SHANNON = ShannonEvaluator

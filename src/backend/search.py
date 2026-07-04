import time
from abc import ABC, abstractmethod
from collections import defaultdict
from enum import Enum

from bulletchess import Board, Move, CHECKMATE, DRAW, FORCED_DRAW

from evaluation import Evaluator


class Search(ABC):
    """Interface for a game-tree search strategy."""

    def __init__(self, evaluator: Evaluator) -> None:
        self.evaluator = evaluator
        self.node_counts: defaultdict[int, int] = defaultdict(int)  # nodes visited, keyed by ply from root
        self.eval_time: float = 0.0  # cumulative time spent in evaluate() (leaf nodes)

    @abstractmethod
    def search(self, board: Board, depth: int, maximizing_player: bool, ply: int = 0) -> tuple[Move | None, float]:
        """Search `board` to `depth` plies and return (best_move, score)."""
        ...

    def evaluate(self, board: Board) -> float:
        """Score a leaf position, tracking cumulative time spent evaluating."""
        start = time.perf_counter()
        score = self.evaluator.evaluate(board)
        self.eval_time += time.perf_counter() - start
        return score

    def is_game_over(self, board: Board) -> bool:
        return board in CHECKMATE or board in DRAW or board in FORCED_DRAW


class NaiveMiniMax(Search):
    """Plain full-width minimax search with no pruning."""

    def search(self, board: Board, depth: int, maximizing_player: bool, ply: int = 0) -> tuple[Move | None, float]:
        self.node_counts[ply] += 1
        if depth == 0 or self.is_game_over(board):
            return None, self.evaluate(board)

        if maximizing_player:
            max_eval = float('-inf')
            best_move: Move | None = None
            for move in board.legal_moves():
                new_board = board.copy()
                new_board.apply(move)
                _, eval_score = self.search(new_board, depth - 1, False, ply + 1)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            return best_move, max_eval
        else:
            min_eval = float('inf')
            best_move: Move | None = None
            for move in board.legal_moves():
                new_board = board.copy()
                new_board.apply(move)
                _, eval_score = self.search(new_board, depth - 1, True, ply + 1)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
            return best_move, min_eval


class SearchAlgorithm(Enum):
    """Selects which Search class Engine uses to pick a move."""
    NAIVE_MINIMAX = NaiveMiniMax

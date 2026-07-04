from bulletchess import Board, Move

from engine.evaluation import EvalFunction
from engine.search import NaiveMiniMax, SearchAlgorithm


def test_naive_minimax_finds_a_mate_in_one():
    """Fool's Mate: 1. f3 e5 2. g4, and now Black has Qh4# available."""
    board = Board()
    for uci in ["f2f3", "e7e5", "g2g4"]:
        board.apply(Move.from_uci(uci))

    search = SearchAlgorithm.NAIVE_MINIMAX.search_class(EvalFunction.SHANNON.eval_class())
    move, _ = search.search(board, depth=1, maximizing_player=False)

    assert move is not None
    assert move.uci() == "d8h4"


def test_search_algorithm_enum_carries_its_implementation_class():
    assert SearchAlgorithm.NAIVE_MINIMAX.search_class is NaiveMiniMax
    assert SearchAlgorithm.NAIVE_MINIMAX == "naive_minimax"

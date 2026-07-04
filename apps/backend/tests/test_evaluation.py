from bulletchess import Board

from engine.evaluation import EvalFunction, ShannonEvaluator


def test_shannon_evaluator_is_zero_at_the_starting_position():
    """Both sides have identical material and mobility at the start, so the
    evaluation should be perfectly symmetric."""
    assert ShannonEvaluator().evaluate(Board()) == 0.0


def test_shannon_evaluator_favors_the_side_with_more_material():
    board = Board.from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPP1/RNBQKBNR w KQkq - 0 1")  # White is down a pawn
    assert ShannonEvaluator().evaluate(board) < 0


def test_eval_function_enum_carries_its_implementation_class():
    assert EvalFunction.SHANNON.eval_class is ShannonEvaluator
    assert EvalFunction.SHANNON == "shannon"

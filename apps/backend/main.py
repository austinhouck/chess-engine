import os
import cmd
import subprocess
from bulletchess import *
from engine import Engine

engine = Engine()

class CLI(cmd.Cmd):
    intro = "Welcome to the interactive shell. Type help or ? to list commands.\n"
    prompt = "chess-engine> "

    def do_set_params(self, arg: str) -> None:
        """Interactively configure search depth, opponent type, and verbose output."""
        # Depth
        depth = input("Depth in plies (default 4): ")
        if not depth:
            engine.depth = 4
        else:
            engine.depth = int(depth)
        # Opponent
        opponent = input("Opponent type (human/computer, default computer): ")
        if not opponent:
            opponent = "computer"
        engine.auto_respond = (opponent.lower() == "computer")
        # Verbose
        verbose = input("Verbose output (y/n, default n): ")
        engine.verbose = (verbose.lower() == "y")
        print(f"Parameters set: depth={engine.depth}, opponent={opponent}")

    def do_show_board(self, arg: str) -> None:
        """Show the current chess board."""
        print(engine.show_board())

    def do_legal_moves(self, arg: str) -> None:
        """Get legal moves for the current board state."""
        print(engine.get_legal_moves())

    def do_move(self, arg: str) -> None:
        """Make a move on the board: move [move]"""
        if arg:
            try:
                engine.make_move(arg)
            except Exception as e:
                print(f"Error making move: {e}")
        else:
            print("Please specify a move.")

    def do_set_opponent(self, arg: str) -> None:
        """Set the opponent type: set_opponent [human/computer]"""
        if arg.lower() == "human":
            engine.auto_respond = False
            print("Opponent set to human.")
        elif arg.lower() == "computer":
            engine.auto_respond = True
            print("Opponent set to computer.")
        else:
            print("Invalid opponent type. Use 'human' or 'computer'.")

    def do_get_evaluation(self, depth: str) -> None:
        """Evaluate the board using minimax algorithm: get_evaluation [depth]"""
        search = engine.search_algorithm.value(engine.eval_function.value())
        _, evaluation = search.search(engine.board, int(depth), True)
        print(f"Board evaluation at depth {depth}: {evaluation}")

    def do_export(self, arg: str) -> None:
        """Export the current game: export [pgn|fen] [filename]"""
        parts = arg.split()
        if not parts:
            print("Please specify a format: export [pgn|fen] [filename]")
            return
        fmt = parts[0].lower()
        filename = parts[1] if len(parts) > 1 else None

        if fmt == "pgn":
            content = engine.export_pgn()
        elif fmt == "fen":
            content = engine.export_fen()
        else:
            print(f"Unknown format: {fmt}. Use 'pgn' or 'fen'.")
            return

        if filename:
            with open(filename, "w") as f:
                f.write(content)
            print(f"Exported {fmt} to {filename}")
        else:
            print(content)

    def do_reset_board(self, arg: str) -> None:
        """Reset the board to the initial state."""
        engine.reset_board()
        print("Board reset to initial state.")

    def do_clear(self, arg: str) -> None:
        """Clear the console screen."""
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

    def do_exit(self, arg: str) -> bool:
        """Exit the application."""
        print("Goodbye!")
        return True  # Returning True stops the cmd loop

if __name__ == "__main__":
    CLI().cmdloop()

# Chess Engine

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/)

`uv` manages everything else — it will create the virtual environment, install
dependencies, and download the pinned Python 3.14 itself if needed. No manual
`venv`/`pip install` step is required.

## Usage

```
./bin/run.sh
```

This launches the interactive CLI (equivalent to `cd src/backend && uv run python main.py`).

## Commands

Also available at any time inside the shell via `help` or `help <command>`.

| Command | Description |
| --- | --- |
| `set_params` | Interactively configure search depth, opponent type, and verbose output. |
| `set_opponent [human\|computer]` | Set the opponent type. |
| `move [move]` | Make a move on the board (SAN or UCI). |
| `show_board` | Show the current chess board. |
| `legal_moves` | List legal moves for the current board state. |
| `get_evaluation [depth]` | Evaluate the board using the minimax algorithm. |
| `export [pgn\|fen] [filename]` | Export the current game as PGN or the current position as FEN. Prints to stdout if no filename is given. |
| `reset_board` | Reset the board to the initial state. |
| `clear` | Clear the console screen. |
| `exit` | Exit the application. |

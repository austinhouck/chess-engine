❯ uv run python main.py
Welcome to the interactive shell. Type help or ? to list commands.

chess-engine> set_params
Depth in plies (default 4):
Opponent type (human/computer, default computer):
Verbose output (y/n, default n): y
Parameters set: depth=4, opponent=computer
chess-engine> move e4
Parsed SAN format move: e2e4
Computer plays: d7d6 with evaluation 3.6000000000000005
Search took 1.59s (1.46s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 20 nodes
  ply 2: 600 nodes
  ply 3: 13160 nodes
  ply 4: 405385 nodes
Board after computer move:
r n b q k b n r
p p p - p p p p
- - - p - - - -
- - - - - - - -
- - - - P - - -
- - - - - - - -
P P P P - P P P
R N B Q K B N R

chess-engine> move nf3
Error making move: Invalid move format: nf3. Use SAN or UCI format.
chess-engine> move Nf3
Parsed SAN format move: g1f3
Computer plays: c7c6 with evaluation 1.1
Search took 2.40s (2.20s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 27 nodes
  ply 2: 755 nodes
  ply 3: 20279 nodes
  ply 4: 602579 nodes
Board after computer move:
r n b q k b n r
p p - - p p p p
- - p p - - - -
- - - - - - - -
- - - - P - - -
- - - - - N - -
P P P P - P P P
R N B Q K B - R

chess-engine> move d4
Parsed SAN format move: d2d4
Computer plays: g8f6 with evaluation 0.10000000000000009
Search took 3.94s (3.61s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 28 nodes
  ply 2: 979 nodes
  ply 3: 27848 nodes
  ply 4: 997632 nodes
Board after computer move:
r n b q k b - r
p p - - p p p p
- - p p - n - -
- - - - - - - -
- - - P P - - -
- - - - - N - -
P P P - - P P P
R N B Q K B - R

chess-engine> move Nc3
Parsed SAN format move: b1c3
Computer plays: d8a5 with evaluation 0.6000000000000001
Search took 5.18s (4.72s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 31 nodes
  ply 2: 1138 nodes
  ply 3: 35210 nodes
  ply 4: 1316105 nodes
Board after computer move:
r n b - k b - r
p p - - p p p p
- - p p - n - -
q - - - - - - -
- - - P P - - -
- - N - - N - -
P P P - - P P P
R - B Q K B - R

chess-engine> move Bd2
Parsed SAN format move: c1d2
Computer plays: a5b6 with evaluation 1.6
Search took 8.67s (7.89s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 43 nodes
  ply 2: 1532 nodes
  ply 3: 60345 nodes
  ply 4: 2169028 nodes
Board after computer move:
r n b - k b - r
p p - - p p p p
- q p p - n - -
- - - - - - - -
- - - P P - - -
- - N - - N - -
P P P B - P P P
R - - Q K B - R

chess-engine> move Rb2
Error making move: Invalid move format: Rb2. Use SAN or UCI format.
chess-engine> move Rb1
Parsed SAN format move: a1b1
^[[CComputer plays: c8g4 with evaluation 1.4
Search took 6.29s (5.72s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 36 nodes
  ply 2: 1218 nodes
  ply 3: 43582 nodes
  ply 4: 1543380 nodes
Board after computer move:
r n - - k b - r
p p - - p p p p
- q p p - n - -
- - - - - - - -
- - - P P - b -
- - N - - N - -
P P P B - P P P
- R - Q K B - R

chess-engine> move Be3
Parsed SAN format move: d2e3
Computer plays: b6b4 with evaluation 0.1
Search took 7.50s (6.83s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 37 nodes
  ply 2: 1360 nodes
  ply 3: 50689 nodes
  ply 4: 1855537 nodes
Board after computer move:
r n - - k b - r
p p - - p p p p
- - p p - n - -
- - - - - - - -
- q - P P - b -
- - N - B N - -
P P P - - P P P
- R - Q K B - R

chess-engine> move a3
Parsed SAN format move: a2a3
Computer plays: b4a5 with evaluation 0.5
Search took 6.92s (6.31s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 40 nodes
  ply 2: 1292 nodes
  ply 3: 51194 nodes
  ply 4: 1731537 nodes
Board after computer move:
r n - - k b - r
p p - - p p p p
- - p p - n - -
q - - - - - - -
- - - P P - b -
P - N - B N - -
- P P - - P P P
- R - Q K B - R

chess-engine> move Bd2
Parsed SAN format move: e3d2
Computer plays: a5b6 with evaluation 1.3
Search took 7.61s (6.90s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 43 nodes
  ply 2: 1411 nodes
  ply 3: 56400 nodes
  ply 4: 1888449 nodes
Board after computer move:
r n - - k b - r
p p - - p p p p
- q p p - n - -
- - - - - - - -
- - - P P - b -
P - N - - N - -
- P P B - P P P
- R - Q K B - R

chess-engine> move Na4
Parsed SAN format move: c3a4
Computer plays: b6c7 with evaluation 1.0
Search took 6.74s (6.14s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 37 nodes
  ply 2: 1284 nodes
  ply 3: 47432 nodes
  ply 4: 1659186 nodes
Board after computer move:
r n - - k b - r
p p q - p p p p
- - p p - n - -
- - - - - - - -
N - - P P - b -
P - - - - N - -
- P P B - P P P
- R - Q K B - R

chess-engine> move Bd3
Parsed SAN format move: f1d3
Computer plays: b8d7 with evaluation 1.0
Search took 6.68s (6.08s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 34 nodes
  ply 2: 1290 nodes
  ply 3: 43628 nodes
  ply 4: 1654239 nodes
Board after computer move:
r - - - k b - r
p p q n p p p p
- - p p - n - -
- - - - - - - -
N - - P P - b -
P - - B - N - -
- P P B - P P P
- R - Q K - - R

chess-engine> move c4
Parsed SAN format move: c2c4
Computer plays: e7e5 with evaluation 0.9
Search took 7.10s (6.46s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 36 nodes
  ply 2: 1331 nodes
  ply 3: 48047 nodes
  ply 4: 1779492 nodes
Board after computer move:
r - - - k b - r
p p q n - p p p
- - p p - n - -
- - - - p - - -
N - P P P - b -
P - - B - N - -
- P - B - P P P
- R - Q K - - R

chess-engine> move d5
Parsed SAN format move: d4d5
Computer plays: f8e7 with evaluation 0.5
Search took 6.75s (6.16s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 35 nodes
  ply 2: 1292 nodes
  ply 3: 45680 nodes
  ply 4: 1689342 nodes
Board after computer move:
r - - - k - - r
p p q n b p p p
- - p p - n - -
- - - P p - - -
N - P - P - b -
P - - B - N - -
- P - B - P P P
- R - Q K - - R

chess-engine> move Nc3
Parsed SAN format move: a4c3
Computer plays: d7c5 with evaluation -0.19999999999999996
Search took 8.51s (7.76s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 39 nodes
  ply 2: 1448 nodes
  ply 3: 56154 nodes
  ply 4: 2126651 nodes
Board after computer move:
r - - - k - - r
p p q - b p p p
- - p p - n - -
- - n P p - - -
- - P - P - b -
P - N B - N - -
- P - B - P P P
- R - Q K - - R

chess-engine> move Bc2
Parsed SAN format move: d3c2
Computer plays: a7a5 with evaluation 0.10000000000000009
Search took 9.45s (8.59s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 46 nodes
  ply 2: 1503 nodes
  ply 3: 66874 nodes
  ply 4: 2318234 nodes
Board after computer move:
r - - - k - - r
- p q - b p p p
- - p p - n - -
p - n P p - - -
- - P - P - b -
P - N - - N - -
- P B B - P P P
- R - Q K - - R

chess-engine> move b4
Parsed SAN format move: b2b4
Computer plays: a5b4 with evaluation -0.2
Search took 10.98s (10.02s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 47 nodes
  ply 2: 1666 nodes
  ply 3: 75089 nodes
  ply 4: 2784965 nodes
Board after computer move:
r - - - k - - r
- p q - b p p p
- - p p - n - -
- - n P p - - -
- p P - P - b -
P - N - - N - -
- - B B - P P P
- R - Q K - - R

chess-engine> move axb4
Parsed SAN format move: a3b4
Computer plays: c5d7 with evaluation 1.1
Search took 11.67s (10.61s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 51 nodes
  ply 2: 1716 nodes
  ply 3: 82640 nodes
  ply 4: 2957576 nodes
Board after computer move:
r - - - k - - r
- p q n b p p p
- - p p - n - -
- - - P p - - -
- P P - P - b -
- - N - - N - -
- - B B - P P P
- R - Q K - - R

chess-engine> move h3
Parsed SAN format move: h2h3
Computer plays: g4h5 with evaluation 1.6
Search took 9.88s (9.00s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 44 nodes
  ply 2: 1588 nodes
  ply 3: 67531 nodes
  ply 4: 2533777 nodes
Board after computer move:
r - - - k - - r
- p q n b p p p
- - p p - n - -
- - - P p - - b
- P P - P - - -
- - N - - N - P
- - B B - P P -
- R - Q K - - R

chess-engine> move Bg5
Parsed SAN format move: d2g5
Computer plays: d7b6 with evaluation 1.9000000000000001
Search took 11.00s (9.97s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 40 nodes
  ply 2: 1687 nodes
  ply 3: 65268 nodes
  ply 4: 2749949 nodes
Board after computer move:
r - - - k - - r
- p q - b p p p
- n p p - n - -
- - - P p - B b
- P P - P - - -
- - N - - N - P
- - B - - P P -
- R - Q K - - R

chess-engine> move c5
Parsed SAN format move: c4c5
Computer plays: d6c5 with evaluation 2.2
Search took 11.65s (10.67s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 40 nodes
  ply 2: 1723 nodes
  ply 3: 67154 nodes
  ply 4: 2893637 nodes
Board after computer move:
r - - - k - - r
- p q - b p p p
- n p - - n - -
- - p P p - B b
- P - - P - - -
- - N - - N - P
- - B - - P P -
- R - Q K - - R

chess-engine> move bxc5
Parsed SAN format move: b4c5
Computer plays: e7c5 with evaluation 2.5
Search took 14.00s (12.78s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 42 nodes
  ply 2: 1893 nodes
  ply 3: 77837 nodes
  ply 4: 3510498 nodes
Board after computer move:
r - - - k - - r
- p q - - p p p
- n p - - n - -
- - b P p - B b
- - - - P - - -
- - N - - N - P
- - B - - P P -
- R - Q K - - R

chess-engine> move Bxf6
Parsed SAN format move: g5f6
Computer plays: h5f3 with evaluation 3.5
Search took 12.31s (11.21s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 42 nodes
  ply 2: 1793 nodes
  ply 3: 74477 nodes
  ply 4: 3194083 nodes
Board after computer move:
r - - - k - - r
- p q - - p p p
- n p - - B - -
- - b P p - - -
- - - - P - - -
- - N - - b - P
- - B - - P P -
- R - Q K - - R

chess-engine> move Qxf3
Parsed SAN format move: d1f3
Computer plays: g7f6 with evaluation 4.9
Search took 11.35s (10.32s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 40 nodes
  ply 2: 1744 nodes
  ply 3: 68143 nodes
  ply 4: 2969780 nodes
Board after computer move:
r - - - k - - r
- p q - - p - p
- n p - - p - -
- - b P p - - -
- - - - P - - -
- - N - - Q - P
- - B - - P P -
- R - - K - - R

chess-engine> move Qxf6
Parsed SAN format move: f3f6
Computer plays: h8g8 with evaluation 5.1000000000000005
Search took 9.75s (8.89s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 37 nodes
  ply 2: 1721 nodes
  ply 3: 55612 nodes
  ply 4: 2469931 nodes
Board after computer move:
r - - - k - r -
- p q - - p - p
- n p - - Q - -
- - b P p - - -
- - - - P - - -
- - N - - - - P
- - B - - P P -
- R - - K - - R

chess-engine> move Rxb6
Parsed SAN format move: b1b6
Computer plays: c5b6 with evaluation 2.4000000000000004
Search took 10.60s (9.66s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 39 nodes
  ply 2: 1827 nodes
  ply 3: 61917 nodes
  ply 4: 2740548 nodes
Board after computer move:
r - - - k - r -
- p q - - p - p
- b p - - Q - -
- - - P p - - -
- - - - P - - -
- - N - - - - P
- - B - - P P -
- - - - K - - R

chess-engine> move O-O
Parsed SAN format move: e1g1
Computer plays: c7e7 with evaluation 0.9
Search took 5.71s (5.20s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 36 nodes
  ply 2: 1331 nodes
  ply 3: 41166 nodes
  ply 4: 1469129 nodes
Board after computer move:
r - - - k - r -
- p - - q p - p
- b p - - Q - -
- - - P p - - -
- - - - P - - -
- - N - - - - P
- - B - - P P -
- - - - - R K -

chess-engine> move Qxe7
Parsed SAN format move: f6e7
Computer plays: e8e7 with evaluation 0.0
Search took 0.08s (0.07s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 1 nodes
  ply 2: 23 nodes
  ply 3: 964 nodes
  ply 4: 21302 nodes
Board after computer move:
r - - - - - r -
- p - - k p - p
- b p - - - - -
- - - P p - - -
- - - - P - - -
- - N - - - - P
- - B - - P P -
- - - - - R K -

chess-engine> move Rb2
Error making move: Invalid move format: Rb2. Use SAN or UCI format.
chess-engine> move Rb1
Parsed SAN format move: f1b1
Computer plays: a8a3 with evaluation 0.3999999999999999
Search took 3.98s (3.58s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 44 nodes
  ply 2: 1149 nodes
  ply 3: 43507 nodes
  ply 4: 1114159 nodes
Board after computer move:
- - - - - - r -
- p - - k p - p
- b p - - - - -
- - - P p - - -
- - - - P - - -
r - N - - - - P
- - B - - P P -
- R - - - - K -

chess-engine> move Rxb6
Parsed SAN format move: b1b6
Computer plays: a3c3 with evaluation 1.9000000000000001
Search took 2.57s (2.30s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 34 nodes
  ply 2: 936 nodes
  ply 3: 28152 nodes
  ply 4: 750328 nodes
Board after computer move:
- - - - - - r -
- p - - k p - p
- R p - - - - -
- - - P p - - -
- - - - P - - -
- - r - - - - P
- - B - - P P -
- - - - - - K -

chess-engine> move Rxb7+
Parsed SAN format move: b6b7
Computer plays: e7d6 with evaluation 0.6000000000000001
Search took 0.28s (0.25s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 5 nodes
  ply 2: 134 nodes
  ply 3: 3520 nodes
  ply 4: 84445 nodes
Board after computer move:
- - - - - - r -
- R - - - p - p
- - p k - - - -
- - - P p - - -
- - - - P - - -
- - r - - - - P
- - B - - P P -
- - - - - - K -

chess-engine> move Bb3
Parsed SAN format move: c2b3
Computer plays: c3c1 with evaluation 0.0
Search took 1.25s (1.12s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 30 nodes
  ply 2: 644 nodes
  ply 3: 17214 nodes
  ply 4: 378600 nodes
Board after computer move:
- - - - - - r -
- R - - - p - p
- - p k - - - -
- - - P p - - -
- - - - P - - -
- B - - - - - P
- - - - - P P -
- - r - - - K -

chess-engine> move Kh2
Parsed SAN format move: g1h2
Computer plays: c1e1 with evaluation 1.2000000000000002
Search took 1.15s (1.02s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 31 nodes
  ply 2: 603 nodes
  ply 3: 16359 nodes
  ply 4: 338677 nodes
Board after computer move:
- - - - - - r -
- R - - - p - p
- - p k - - - -
- - - P p - - -
- - - - P - - -
- B - - - - - P
- - - - - P P K
- - - - r - - -

chess-engine> move f3
Parsed SAN format move: f2f3
Computer plays: e1e2 with evaluation -1.1
Search took 0.95s (0.85s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 30 nodes
  ply 2: 553 nodes
  ply 3: 14692 nodes
  ply 4: 288069 nodes
Board after computer move:
- - - - - - r -
- R - - - p - p
- - p k - - - -
- - - P p - - -
- - - - P - - -
- B - - - P - P
- - - - r - P K
- - - - - - - -

chess-engine> move Bc4
Parsed SAN format move: b3c4
Computer plays: e2g2 with evaluation -2.6
Search took 1.27s (1.13s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 29 nodes
  ply 2: 651 nodes
  ply 3: 17156 nodes
  ply 4: 374512 nodes
Board after computer move:
- - - - - - r -
- R - - - p - p
- - p k - - - -
- - - P p - - -
- - B - P - - -
- - - - - P - P
- - - - - - r K
- - - - - - - -

chess-engine> move Kh1
Parsed SAN format move: h2h1
Computer plays: g2g1 with evaluation -200.0
Search took 1.25s (1.12s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 32 nodes
  ply 2: 682 nodes
  ply 3: 19010 nodes
  ply 4: 375075 nodes
Board after computer move:
- - - - - - r -
- R - - - p - p
- - p k - - - -
- - - P p - - -
- - B - P - - -
- - - - - P - P
- - - - - - - -
- - - - - - r K

chess-engine> move Kh2
Parsed SAN format move: h1h2
Computer plays: g8g2 with evaluation -200.0
Search took 1.29s (1.15s in evaluate_board)
  ply 0: 1 nodes
  ply 1: 33 nodes
  ply 2: 684 nodes
  ply 3: 19320 nodes
  ply 4: 381249 nodes
Board after computer move:
- - - - - - - -
- R - - - p - p
- - p k - - - -
- - - P p - - -
- - B - P - - -
- - - - - P - P
- - - - - - r K
- - - - - - r -

chess-engine>

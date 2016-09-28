# GAME RULE
1. The game board is a 5x5 grid representing territories the two parties will trample.
2. Each party takes turns as in chess or tic-tac-toe manner. That is, the first party takes a move, then the second party, then back to the first party and so forth.
3. Each square has a fixed point value between 1 and 99.
4. The values of the squares can be changed for each game, but remain constant within a game.
5. The objective of the game for each party is to score the most points, i.e. the total point value of all his or her occupied square. Thus, one wants to capture the squares worth the most points.
6. The game ends when all square are occupied, because no more moves are left.
7. On each turn, a player can make one of two moves:
    - **Raid**: You can take over any unoccupied square that is adjacent to one of your current pieces (horizontally or vertically, but not diagonally). You place a new piece in the taken over square. Also, any enemy pieces adjacent to your new piece (horizontally or vertically, but not diagonally) are conquered and replaced by your own pieces. You can **Raid** a square even if there are no enemy pieces adjacent to it to be conquered. Once you have made this move, your turn is over.
    - **Sneak**: You can take any unoccupied square on the board that is not next to your existing pieces. This will create a new piece on the board. Unlike **Raid** which is an aggressive move, **Sneak** is a covert operation, so it won’t conquer any enemy pieces. It simply allows one to place a piece at an unoccupied square that is not reachable by **Raid**
8. **Notice that a space that can be Raided cannot be Sneaked.** Once you have done a **Sneak**, your turn is complete.
9. Again, the **Raid** operation has two effects: (1) A new piece is created in the target square, and (2) any enemy pieces adjacent to the target square are turned to the player’s side. On the other hand, **Sneak** has only effect (1).
0. Any unoccupied square can be taken with either **Raid** or **Sneak**, but they are mutuallyexclusive. If the square is horizontally or vertically adjacent to an existing selfowned piece, it’s a **Raid**. Otherwise it’s a **Sneak**.
1. Anytime adjacency is checked (e.g. **Raid** validity, conquering enemy pieces), it's always checking vertical and horizontal neighbors, but never diagonal. In other words, a diagonal neighbor is never considered adjacent.

# Input File Format
For each test case, you are provided with an input file that describes the current state of the game. In the input and output files, the two sides will be represented as X and O.
```
<task#>
Greedy Bestfirst
Search = 1, MiniMax = 2, Alphabeta
Pruning = 3
<your player> X or O
<cutting off depth>
Cutoff
depth started from the root.
<board grid value>
Positive integers from 1 99
5 in each row separated with a space, 5 total rows
<current board state>
*: Unoccupied
X: Player 1
O: Player 2
5 in each row, no space in between, 5 total rows
The ordering corresponds with the board values.
```

An input example is as blow:
```
2
X
2
20 16 1 32 30
20 12 2 11 8
28 48 9 1 1
20 12 10 6 2
25 30 23 21 10
**XX*
**XOX
***O*
**OO*
```

# Output Format
For each test case, your program should output a file named *next_state.txt* showing the next state of the board after the move. For Minimax and AlphaBeta
Pruning , your program should output another file named *traverse_log.txt* showing the traverse log of your program in the following format. There is no need to output *traverse_log.txt* for Greedy Bestfirst Search.

# Usage
This program should be called as `$python .\file_name.py -i input_file_name.txt`
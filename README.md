Tic Tac Toe game; currently supporting all 6 uninformed search algos; inspired by Charley Lewittes in [his gist](https://gist.github.com/ctlewitt/34986ab411b49c5fdce7)
<br/>

### UPDATE
It now supports six different uninformed search algorithms,

1. **Breadth-First Search (BFS)**
   - Explores all moves at the current depth before going deeper
   - Good for finding the shortest path to a win
   - Explores moves level by level

2. **Depth-First Search (DFS)**
   - Explores one path to its conclusion before backtracking
   - Can find winning sequences quickly but might not find the shortest path
   - Uses less memory than BFS

3. **Uniform Cost Search (UCS)**
   - Similar to BFS but considers move costs
   - Assigns lower costs to moves that could lead to winning
   - Higher costs to moves that might lead to losing

4. **Iterative Deepening Search (IDS)**
   - Combines benefits of DFS and BFS
   - Gradually increases search depth
   - Guarantees finding the optimal solution at the current depth

5. **Bidirectional Search**
   - Searches from both current state and goal states
   - Can find winning paths more efficiently
   - Meets in the middle to find solutions

6. **Depth-Limited Search (DLS)**
   - DFS with a maximum depth limit
   - Prevents searching too deep
   - Good for quick decision making

<br/>
<br/>
<br/>
<br/>
<br/>

#### OLD SUPPORT

It supports minimax algorithm for the computer opponent. Its a type of uninformed search that:

explores all possible future game states (levels in trees)
assigns scores to end states (+1 for computer win, -1 for human win, 0 for draw)
works backward to choose moves that maximize the computer's minimum guaranteed score
ps: part of uni asgmt*
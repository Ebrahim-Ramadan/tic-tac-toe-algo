import copy
from collections import deque
import heapq

class GameState:
    def __init__(self, board, player, depth=0, parent=None, move=None):
        self.board = board
        self.player = player  # Current player's turn (X or O)
        self.depth = depth    # Current depth in search tree
        self.parent = parent  # Parent state
        self.move = move      # Move that led to this state
        
    def get_empty_cells(self):
        empty = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == " ":
                    empty.append((i, j))
        return empty
    
    def is_winner(self, player):
        # Check rows
        for row in self.board:
            if all(cell == player for cell in row):
                return True
                
        # Check columns
        for col in range(len(self.board[0])):
            if all(self.board[row][col] == player for row in range(len(self.board))):
                return True
                
        # Check diagonals
        if all(self.board[i][i] == player for i in range(len(self.board))):
            return True
        if all(self.board[i][len(self.board)-1-i] == player for i in range(len(self.board))):
            return True
            
        return False
    
    def is_terminal(self):
        return self.is_winner('X') or self.is_winner('O') or not self.get_empty_cells()
    
    def make_move(self, move, player):
        new_board = [row[:] for row in self.board]
        new_board[move[0]][move[1]] = player
        return GameState(new_board, 'O' if player == 'X' else 'X', self.depth + 1, self, move)

class SearchAlgorithms:
    @staticmethod
    def breadth_first_search(initial_state, computer_player):
        """
        BFS: Explores all states at current depth before moving deeper
        Returns: Best move found using BFS
        """
        queue = deque([(initial_state, [])])
        visited = set()
        
        while queue:
            current_state, path = queue.popleft()
            board_tuple = tuple(map(tuple, current_state.board))
            
            if board_tuple in visited:
                continue
                
            visited.add(board_tuple)
            
            # If we found a winning state, return the first move that led there
            if current_state.is_winner(computer_player):
                return path[0] if path else None
                
            # Add all possible next states to queue
            for move in current_state.get_empty_cells():
                next_state = current_state.make_move(move, current_state.player)
                new_path = path + [move] if path else [move]
                queue.append((next_state, new_path))
        
        # If no winning path found, return first available move
        return initial_state.get_empty_cells()[0] if initial_state.get_empty_cells() else None

    @staticmethod
    def depth_first_search(initial_state, computer_player, depth_limit=None):
        """
        DFS: Explores deep into the game tree before backtracking
        Returns: Best move found using DFS
        """
        def dfs_recursive(state, depth):
            if depth_limit and depth >= depth_limit:
                return None
                
            if state.is_winner(computer_player):
                return state.move
                
            for move in state.get_empty_cells():
                next_state = state.make_move(move, state.player)
                result = dfs_recursive(next_state, depth + 1)
                if result is not None:
                    return move
            return None
            
        return dfs_recursive(initial_state, 0)

    @staticmethod
    def uniform_cost_search(initial_state, computer_player):
        """
        UCS: Explores states based on path cost
        Returns: Best move found using UCS
        """
        def calculate_cost(state):
            # Lower cost for states that block opponent's winning moves
            # or create winning opportunities
            cost = state.depth
            opponent = 'O' if computer_player == 'X' else 'X'
            
            if state.is_winner(computer_player):
                return -1000  # Very low cost for winning states
            elif state.is_winner(opponent):
                return 1000   # Very high cost for losing states
                
            return cost
            
        priority_queue = [(0, id(initial_state), initial_state, None)]
        visited = set()
        
        while priority_queue:
            cost, _, current_state, first_move = heapq.heappop(priority_queue)
            board_tuple = tuple(map(tuple, current_state.board))
            
            if board_tuple in visited:
                continue
                
            visited.add(board_tuple)
            
            if current_state.is_winner(computer_player):
                return first_move
                
            for move in current_state.get_empty_cells():
                next_state = current_state.make_move(move, current_state.player)
                new_cost = calculate_cost(next_state)
                new_first_move = first_move if first_move else move
                heapq.heappush(priority_queue, 
                              (new_cost, id(next_state), next_state, new_first_move))
        
        return initial_state.get_empty_cells()[0] if initial_state.get_empty_cells() else None

    @staticmethod
    def iterative_deepening_search(initial_state, computer_player, max_depth=9):
        """
        IDS: Gradually increases depth limit of DFS
        Returns: Best move found using IDS
        """
        for depth in range(max_depth):
            result = SearchAlgorithms.depth_first_search(initial_state, computer_player, depth)
            if result is not None:
                return result
        return initial_state.get_empty_cells()[0] if initial_state.get_empty_cells() else None

    @staticmethod
    def bidirectional_search(initial_state, computer_player):
        """
        Bidirectional: Searches from both initial and goal states
        Returns: Best move found using bidirectional search
        """
        # Forward search from initial state
        forward_queue = deque([(initial_state, [])])
        forward_visited = set()
        
        # Backward search from goal states
        goal_states = []
        # Create some sample goal states (winning configurations)
        for i in range(len(initial_state.board)):
            goal_board = [[" " for _ in range(len(initial_state.board))] for _ in range(len(initial_state.board))]
            # Create horizontal win
            goal_board[i] = [computer_player] * len(initial_state.board)
            goal_states.append(GameState(goal_board, computer_player))
            
        backward_queues = [(deque([(goal_state, [])]), set()) for goal_state in goal_states]
        
        while forward_queue and any(bq[0] for bq in backward_queues):
            # Forward search step
            current_state, path = forward_queue.popleft()
            board_tuple = tuple(map(tuple, current_state.board))
            
            if board_tuple in forward_visited:
                continue
                
            forward_visited.add(board_tuple)
            
            # Check if we've met in the middle
            for _, backward_visited in backward_queues:
                if board_tuple in backward_visited:
                    return path[0] if path else None
                    
            # Add next states to forward queue
            for move in current_state.get_empty_cells():
                next_state = current_state.make_move(move, current_state.player)
                new_path = path + [move] if path else [move]
                forward_queue.append((next_state, new_path))
            
            # Backward search step for each goal state
            for backward_queue, backward_visited in backward_queues:
                if backward_queue:
                    current_state, path = backward_queue.popleft()
                    board_tuple = tuple(map(tuple, current_state.board))
                    
                    if board_tuple in backward_visited:
                        continue
                        
                    backward_visited.add(board_tuple)
                    
                    if board_tuple in forward_visited:
                        return path[0] if path else None
                    
                    # Add previous states to backward queue
                    for move in current_state.get_empty_cells():
                        prev_state = current_state.make_move(move, current_state.player)
                        new_path = path + [move] if path else [move]
                        backward_queue.append((prev_state, new_path))
        
        return initial_state.get_empty_cells()[0] if initial_state.get_empty_cells() else None

    @staticmethod
    def depth_limited_search(initial_state, computer_player, depth_limit=3):
        """
        DLS: DFS with a depth limit
        Returns: Best move found using DLS
        """
        return SearchAlgorithms.depth_first_search(initial_state, computer_player, depth_limit)

class TicTacToeWithSearch:
    def __init__(self, size=3):
        self.size = size
        self.board = [[" " for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'
        self.search_algorithm = SearchAlgorithms.breadth_first_search  # Default algorithm
        
    def available_algorithms(self):
        return {
            1: ("Breadth-First Search", SearchAlgorithms.breadth_first_search),
            2: ("Depth-First Search", SearchAlgorithms.depth_first_search),
            3: ("Uniform Cost Search", SearchAlgorithms.uniform_cost_search),
            4: ("Iterative Deepening Search", SearchAlgorithms.iterative_deepening_search),
            5: ("Bidirectional Search", SearchAlgorithms.bidirectional_search),
            6: ("Depth-Limited Search", SearchAlgorithms.depth_limited_search)
        }
        
    def set_search_algorithm(self, algorithm_number):
        algorithms = self.available_algorithms()
        if algorithm_number in algorithms:
            self.search_algorithm = algorithms[algorithm_number][1]
            return algorithms[algorithm_number][0]
        return None

    def make_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def computer_move(self, computer_player):
        current_state = GameState(self.board, self.current_player)
        move = self.search_algorithm(current_state, computer_player)
        
        if move:
            self.make_move(move[0], move[1])
            return move
        return None

    def print_board(self):
        for row in self.board:
            print("|" + "|".join(row) + "|")
            print("-" * (self.size * 2 + 1))

# Example usage:
def play_game():
    game = TicTacToeWithSearch()
    print("Available search algorithms:")
    for num, (name, _) in game.available_algorithms().items():
        print(f"{num}. {name}")
    
    algo_choice = int(input("Choose search algorithm (1-6): "))
    algo_name = game.set_search_algorithm(algo_choice)
    print(f"Using {algo_name}")
    
    computer_player = 'O'
    human_player = 'X'
    
    while True:
        game.print_board()
        
        # Human move
        if game.current_player == human_player:
            row = int(input("Enter row (0-2): "))
            col = int(input("Enter column (0-2): "))
            if not game.make_move(row, col):
                print("Invalid move, try again")
                continue
        # Computer move
        else:
            print("Computer's turn...")
            move = game.computer_move(computer_player)
            if not move:
                print("Game over!")
                break
                
        current_state = GameState(game.board, game.current_player)
        if current_state.is_winner('X'):
            print("X (you) wins!")
            break
        elif current_state.is_winner('O'):
            print("O (computer) wins!")
            break
        elif not current_state.get_empty_cells():
            print("Draw!")
            break

if __name__ == "__main__":
    play_game()
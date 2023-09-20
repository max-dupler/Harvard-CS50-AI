X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    new_board = [row[:] for row in board]
    if new_board[i][j] is not EMPTY:
        raise Exception("Invalid action")
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows, columns, and diagonals for a winner
    for player_symbol in [X, O]:
        for i in range(3):
            if all(cell == player_symbol for cell in board[i]):
                return player_symbol
            if all(board[j][i] == player_symbol for j in range(3)):
                return player_symbol
        if all(board[i][i] == player_symbol for i in range(3)) or \
           all(board[i][2 - i] == player_symbol for i in range(3)):
            return player_symbol
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result == X:
        return 1
    elif result == O:
        return -1
    return 0


def minimax(board, alpha=float('-inf'), beta=float('inf')):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    curr_player = player(board)
    if curr_player == X:
        max_utility = float('-inf')
        best_action = None
        for action in actions(board):
            new_utility = min_value(result(board, action), alpha, beta)
            if new_utility > max_utility:
                max_utility = new_utility
                best_action = action
            alpha = max(alpha, max_utility)
            if beta <= alpha:
                break
        return best_action
    else:
        min_utility = float('inf')
        best_action = None
        for action in actions(board):
            new_utility = max_value(result(board, action), alpha, beta)
            if new_utility < min_utility:
                min_utility = new_utility
                best_action = action
            beta = min(beta, min_utility)
            if beta <= alpha:
                break
        return best_action


def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return v


def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break
    return v

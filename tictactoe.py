"""
Tic Tac Toe Player
"""

import math
import copy

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
    count_X = 0
    count_O = 0
    count_EMPTY = 0
    for row in board:
        for mark in row:
            if mark == X:
                count_X += 1
            elif mark == O:
                count_O += 1
            else:
                count_EMPTY += 1
    if count_EMPTY == 9:
        return X
    elif terminal(board):
        return None
    elif count_X > count_O:
        return O
    else:
        return X
                
        


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    set_of_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                set_of_actions.add((i,j))
                
    return set_of_actions


    
    
    



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]
    assert (board[i][j] == EMPTY), "Invalid action input"
    answer_board = copy.deepcopy(board)
    next_player = player(board)
    if next_player is not None:
        answer_board[i][j]=next_player
    return answer_board


    

    
        


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    assert board is not None, "Board is None"
    def is_winning_diagonal(my_set):
        for i in range(3):
            if (i,i) not in my_set:
                return False
        return True
    
    def is_winning_anti_diagonal(my_set):
        for i in range(3):
            if (i,2-i) not in my_set:
                return False
        return True
    
    def is_winning_row(my_set):
        for i in range(3):
            winning = True
            for j in range(3):
                if (i,j) not in my_set:
                    winning = False
                    break
            else:
                return True
        return False
    
    def is_winning_col(my_set):
        for j in range(3):
            winning = True
            for i in range(3):
                if (i,j) not in my_set:
                    winning = False
                    break
            else:
                return True
        return False
              
    def is_winning(my_set):
        return is_winning_row(my_set) or is_winning_col(my_set) or is_winning_diagonal(my_set) or is_winning_anti_diagonal(my_set)
    
    cells_of_X = set()
    cells_of_O = set()
 
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                cells_of_X.add((i,j))
            elif board[i][j] == O:
                cells_of_O.add((i,j))
                
    if is_winning(cells_of_X):
        return X
    elif is_winning(cells_of_O):
        return O
    else:
        return None

 
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board)!= None:
        return True
    
    for row in board:
        for mark in row:
            if mark == EMPTY:
                return False
            
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    try:
        assert(terminal(board))
        if winner(board) == None:
            return 0
        elif winner(board) == X:
            return 1
        else:
            return -1
        
    except AssertionError:
        print("Board is not terminal")
        return None
        



#alpha -  minimum score that the maximizing player is assured of (initially -inf)
#beta - maximum score that the minimizing player is assured of (initially +inf)



def max_value(board, alpha, beta):
    if terminal(board):
        return (utility(board), None)
    winning_action = None
    score = -math.inf
    set_of_actions = actions(board)
    for action in set_of_actions:
        #score = max(score, min_value(result(board, action)))
        new_score, new_move =  min_value(result(board, action), alpha, beta)
        if new_score > score:
            winning_action = action
            score = new_score
        alpha = max(score, alpha)
        if alpha >= beta:
            break
        #if score == 1:
            #break
    return (score, winning_action)


def min_value(board, alpha, beta):
    if terminal(board):
        return (utility(board), None)
    winning_action = None
    score = math.inf
    set_of_actions = actions(board)
    for action in set_of_actions:
        #score = min(score, max_value(result(board, action)))
        new_score, new_move =  max_value(result(board, action), alpha, beta)
        if new_score < score:
            winning_action = action
            score = new_score
        beta = min(score, beta)
        if alpha >= beta:
            break
        #if score == -1:
            #break
    return (score, winning_action)



    
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None    
    if player(board) == X:
        score, winning_action = max_value(board, -math.inf, math.inf)
    elif player(board) == O:
        score, winning_action = min_value(board, -math.inf, math.inf)
    return winning_action

    
            
        
 

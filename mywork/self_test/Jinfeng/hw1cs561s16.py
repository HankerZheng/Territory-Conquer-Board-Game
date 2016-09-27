
__author__ = "Jinfeng Pan"

import copy
import sys


class Board(object):
    def __init__(self, player1, player2, cut_off_depth, states, values):
        self.player1 = player1
        self.player2 = player2
        self.turn = player1  # it's player1's turn at the first
        self.depth = 0  # the depth is maximum to cut-off depth
        self.cut_off_depth = cut_off_depth
        self.states = states
        self.values = values
        self.minimax_traverse_log = ['root', 0, float('-inf')]
        self.alpha_beta_traverse_log = ['root', 0, float('-inf'), float('-inf'), float('inf')]
        self.blank_grid = []  # represent all blank grids
        self.evaluation_value = 0
        # initialize evaluation value and blank grids
        for row in range(5):
            for col in range(5):
                if self.states[row][col] == player1:
                    self.evaluation_value += values[row][col]
                elif self.states[row][col] == player2:
                    self.evaluation_value -= values[row][col]
                else:
                    self.blank_grid.append([row, col])

    # return blank grids as a list
    def get_blank_grid(self):
        return self.blank_grid

    # return board state as a list
    def get_states(self):
        return self.states

    # return minimax traverse log
    def get_minimax_traverse_log(self):
        return self.minimax_traverse_log

    # return alpha beta search traverse log
    def get_alpha_beta__traverse_log(self):
        return self.alpha_beta_traverse_log

    # change the Board object for the action taken, separate for minimax and alpha-beta
    def next_state(self, action, evaluation, occupy_grids):
        self.blank_grid.remove(action)
        self.evaluation_value = evaluation
        for grid in occupy_grids:
            self.states[grid[0]][grid[1]] = self.turn
        self.turn = self.player2 if self.turn == self.player1 else self.player1

    def minimax_next_state(self, action, evaluation, occupy_grids):
        self.next_state(action, evaluation, occupy_grids)
        self.minimax_traverse_log = [action, self.depth, evaluation]

    def alpha_beta_next_state(self, action, evaluation, occupy_grids, alpha, beta):
        self.next_state(action, evaluation, occupy_grids)
        self.alpha_beta_traverse_log = [action, self.depth, evaluation, alpha, beta]


# get new evaluation value and grids taken by the player caused by the action
def get_evaluation(evaluation, values, states, action, p, turn):
    if turn == p:
        evaluation += values[action[0]][action[1]]
    else:
        evaluation -= values[action[0]][action[1]]
    occupy_grids = [[action[0], action[1]]]
    if is_next(action, states, turn):
        evaluation, occupy_grids = raid(action, values, states, evaluation, occupy_grids, p, turn)
    return evaluation, occupy_grids


# check if the grid chosen to take action is next to any current grids of the player
def is_next(action, states, turn):
    for row in range(action[0] - 1, action[0] + 2):
        for col in range(action[1] - 1, action[1] + 2):
            if row in range(5) and col in range(5) and abs(row + col - action[0] - action[1]) == 1:
                if states[row][col] == turn:
                    return True
    return False


# raid the other player's grids next to the action and return new evaluation value and occupied grids
def raid(action, values, states, evaluation, occupy_grids, p, turn):
    for row in range(action[0] - 1, action[0] + 2):
        for col in range(action[1] - 1, action[1] + 2):
            if row in range(5) and col in range(5) and abs(row + col - action[0] - action[1]) == 1:
                if states[row][col] != turn and states[row][col] != '*':
                    if turn == p:
                        evaluation += 2 * values[row][col]
                    else:
                        evaluation -= 2 * values[row][col]
                    occupy_grids.append([row, col])
    return evaluation, occupy_grids


# get the traverse log of string format
def get_traverse_log(traverse_log):
    grid = ''
    if traverse_log[0] == 'root':
        grid = 'root'
    else:
        grid_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
        grid = grid_dict[traverse_log[0][1]] + str(traverse_log[0][0] + 1)
    depth = str(traverse_log[1])
    log = grid + ',' + depth + ','
    for i in range(2, len(traverse_log)):
        if traverse_log[i] == float('inf'):
            log += 'Infinity,'
        elif traverse_log[i] == float('-inf'):
            log += '-Infinity,'
        else:
            log += str(traverse_log[i]) + ','
    return log[0: len(log) - 1]


# check if the game is over for all grids are occupied or the depth is up to cut-off
def game_terminal(board):
    if board.depth == board.cut_off_depth:
        return True
    for i in range(5):
        for j in range(5):
            if board.states[i][j] == '*':
                return False
    return True


""" Greedy Best first Search """


def greedy_best_first_search(board):
    actions = board.get_blank_grid()
    best_action = actions[0]
    best_score = float('-inf')
    occupy = []
    for action in actions:
        evaluation, occupy_grids = get_evaluation(board.evaluation_value, board.values, board.states, action,
                                                  board.player1, board.turn)
        if evaluation > best_score:
            best_action = action
            best_score = evaluation
            occupy = copy.copy(occupy_grids)
    board.next_state(best_action, best_score, occupy)
    return board.get_states()


""" Minimax """


def minimax(board):
    global traverse_flag
    if traverse_flag:
        global traverse_log_file
        traverse_log_file.write('Node,Depth,Value')
    # write_traverse_log('Node,Depth,Value')
    best_score, best_action = max_play(board)
    evaluation, occupy_grids = get_evaluation(board.evaluation_value, board.values, board.states, best_action,
                                              board.player1, board.turn)
    board.minimax_next_state(best_action, evaluation, occupy_grids)
    return board.get_states()


def max_play(board):
    if game_terminal(board):
        write_traverse_log(get_traverse_log(board.get_minimax_traverse_log()))
        return board.evaluation_value, [0, 0]
    board.depth += 1
    best_score = float('-inf')
    best_action = [0, 0]
    board.minimax_traverse_log[2] = best_score
    write_traverse_log(get_traverse_log(board.get_minimax_traverse_log()))

    actions = board.get_blank_grid()
    for action in actions:
        clone = copy.deepcopy(board)
        evaluation, occupy_grids = get_evaluation(board.evaluation_value, board.values, board.states, action,
                                                  board.player1, board.turn)
        clone.minimax_next_state(action, evaluation, occupy_grids)
        score, a = min_play(clone)
        if score > best_score:
            best_action = action
            best_score = score
        board.minimax_traverse_log[2] = best_score
        write_traverse_log(get_traverse_log(board.get_minimax_traverse_log()))
    return best_score, best_action


def min_play(board):
    if game_terminal(board):
        write_traverse_log(get_traverse_log(board.get_minimax_traverse_log()))
        return board.evaluation_value, [0, 0]
    board.depth += 1
    best_score = float('inf')
    best_action = [0, 0]
    board.minimax_traverse_log[2] = best_score
    write_traverse_log(get_traverse_log(board.get_minimax_traverse_log()))

    actions = board.get_blank_grid()
    for action in actions:
        clone = copy.deepcopy(board)
        evaluation, occupy_grids = get_evaluation(board.evaluation_value, board.values, board.states, action,
                                                  board.player1, board.turn)
        clone.minimax_next_state(action, evaluation, occupy_grids)
        score, a = max_play(clone)
        if score < best_score:
            best_action = action
            best_score = score
        board.minimax_traverse_log[2] = best_score
        write_traverse_log(get_traverse_log(board.get_minimax_traverse_log()))
    return best_score, best_action


""" Alpha Beta Pruning """


def alpha_beta_search(board):
    global traverse_flag
    if traverse_flag:
        global traverse_log_file
        traverse_log_file.write('Node,Depth,Value,Alpha,Beta')
    # write_traverse_log('Node,Depth,Value,Alpha,Beta')
    best_score, best_action = max_value(board, float('-inf'), float('inf'))
    evaluation, occupy_grids = get_evaluation(board.evaluation_value, board.values, board.states, best_action,
                                              board.player1, board.turn)
    board.alpha_beta_next_state(best_action, evaluation, occupy_grids, float('-inf'), float('inf'))
    return board.get_states()


def max_value(board, alpha, beta):
    if game_terminal(board):
        write_traverse_log(get_traverse_log(board.get_alpha_beta__traverse_log()))
        return board.evaluation_value, [0, 0]
    board.depth += 1
    best_score = float('-inf')
    best_action = [0, 0]
    board.alpha_beta_traverse_log[2] = best_score
    write_traverse_log(get_traverse_log(board.get_alpha_beta__traverse_log()))

    actions = board.get_blank_grid()
    for action in actions:
        clone = copy.deepcopy(board)
        evaluation, occupy_grids = get_evaluation(board.evaluation_value, board.values, board.states, action,
                                                  board.player1, board.turn)
        clone.alpha_beta_next_state(action, evaluation, occupy_grids, alpha, beta)
        score, a = min_value(clone, alpha, beta)
        if score > best_score:
            best_action = action
            best_score = score
        board.alpha_beta_traverse_log[2] = best_score
        if best_score >= beta:
            write_traverse_log(get_traverse_log(board.get_alpha_beta__traverse_log()))
            return best_score, [0, 0]
        alpha = max(alpha, best_score)
        board.alpha_beta_traverse_log[3] = alpha
        write_traverse_log(get_traverse_log(board.get_alpha_beta__traverse_log()))
    return best_score, best_action


def min_value(board, alpha, beta):
    if game_terminal(board):
        write_traverse_log(get_traverse_log(board.get_alpha_beta__traverse_log()))
        return board.evaluation_value, [0, 0]
    board.depth += 1
    best_score = float('inf')
    best_action = [0, 0]
    board.alpha_beta_traverse_log[2] = best_score
    write_traverse_log(get_traverse_log(board.get_alpha_beta__traverse_log()))

    actions = board.get_blank_grid()
    for action in actions:
        clone = copy.deepcopy(board)
        evaluation, occupy_grids = get_evaluation(board.evaluation_value, board.values, board.states, action,
                                                  board.player1, board.turn)
        clone.alpha_beta_next_state(action, evaluation, occupy_grids, alpha, beta)
        score, a = max_value(clone, alpha, beta)
        if score < best_score:
            best_action = action
            best_score = score
        board.alpha_beta_traverse_log[2] = best_score
        if best_score <= alpha:
            write_traverse_log(get_traverse_log(board.get_alpha_beta__traverse_log()))
            return best_score, [0, 0]
        beta = min(beta, best_score)
        board.alpha_beta_traverse_log[4] = beta
        write_traverse_log(get_traverse_log(board.get_alpha_beta__traverse_log()))
    return best_score, best_action


# write traverse log into file
def write_traverse_log(log_str):
    global traverse_flag
    if traverse_flag:
        global traverse_log_file
        traverse_log_file.write('\n' + log_str)


# play the game according to specific method and cut-off and return next state as list
def next_move_game(p1, p2, method, cut_off_depth, states, values):
    board = Board(p1, p2, cut_off_depth, states, values)
    if method == 1:
        next_state = greedy_best_first_search(board)
    elif method == 2:
        next_state = minimax(board)
    elif method == 3:
        next_state = alpha_beta_search(board)
    return next_state


# check if all the grids are occupied
def all_occupied(states):
    for i in range(5):
        for j in range(5):
            if states[i][j] == '*':
                return False
    return True


""" Read Input File """

input_file = open(sys.argv[2], 'rU')
# input_file = open('input3.txt', 'rU')
lines = input_file.readlines()
input_file.close()

board_values = []
board_states = []

traverse_flag = True

if len(lines) == 13:  # guide your squirrel warriors next move
    method = int(lines[0].strip())
    if not method == 1:
        traverse_log_file = open('traverse_log.txt', 'w')
    else:
        traverse_flag = False
    player = lines[1].strip()
    depth = int(lines[2].strip())
    for i in range(3, 8):
        val = lines[i].strip().split(' ')
        x = [int(x) for x in val]
        board_values.append(x)
    for j in range(8, 13):
        board_states.append(list(lines[j].strip()))
    if player == 'X':
        p1, p2 = 'X', 'O'
    else:
        p1, p2 = 'O', 'X'

    next_state_file = open('next_state.txt', 'w')
    next_state = next_move_game(p1, p2, method, depth, board_states, board_values)
    for i in range(4):
        next_state_file.write(''.join(next_state[i]) + '\n')
    next_state_file.write(''.join(next_state[4]))
    if traverse_flag:
        traverse_log_file.close()
    next_state_file.close()

elif len(lines) == 17:  # guide your squirrel warriors next move
    traverse_flag = False
    p1 = lines[1].strip()
    method1 = int(lines[2].strip())
    depth1 = int(lines[3].strip())
    p2 = lines[4].strip()
    method2 = int(lines[5].strip())
    depth2 = int(lines[6].strip())
    for i in range(7, 12):
        val = lines[i].strip().split(' ')
        x = [int(x) for x in val]
        board_values.append(x)
    for j in range(12, 17):
        board_states.append(list(lines[j].strip()))
    trace_state_file = open('trace_state.txt', 'w')
    method = method1
    depth = depth1
    first_line = True
    while not all_occupied(board_states):
        next_state = next_move_game(p1, p2, method, depth, board_states, board_values)
        for i in range(5):
            if first_line:
                trace_state_file.write(''.join(next_state[i]))
                first_line = False
            else:
                trace_state_file.write('\n' + ''.join(next_state[i]))
        p1, p2 = p2, p1
        depth = depth2 if depth == depth1 else depth1
        method = method2 if method == method1 else method1
        board_states = copy.copy(next_state)
    trace_state_file.close()

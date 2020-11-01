# 2020 - Cyril Gremaud / Rafael Urben
### Imports

from tqdm import tqdm

# board = [
#     [0, 6, 12, 18, 24, 30, 36],
#     [1, 7, 13, 19, 25, 31, 37],
#     [2, 8, 14, 20, 26, 32, 38],
#     [3, 9, 15, 21, 27, 33, 39],
#     [4, 10, 16, 22, 28, 34, 40],
#     [5, 11, 17, 23, 29, 35, 41],
# ]

board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]


def print_board(board):
    for i in range(len(board)):
        print(board[i])
    print("")

def drop_a(board, position):
    board.reverse()
    for i in range(len(board)):
        if board[i][position] == 0:
            board[i][position] = 1
            board.reverse()
            #print_board(board)
            return board

def drop_b(board, position):
    board.reverse()
    for i in range(len(board)):
        if board[i][position] == 0:
            board[i][position] = 2
            board.reverse()
            #print_board(board)
            return board


def get_lines(board):
    lines = board    #horizontal lines


    #verical lines
    vertical_lines = []
    for i in range(len(board[0])):
        vertical_line = []
        for j in range(len(board)):
            vertical_line.append(board[j][i])
        vertical_lines.append(vertical_line)


    #diagonal lines
    diagonal_lines = []
    for i in range(len(board[0])-3):
        diagonal_line = []
        for j in range(len(board)):
            if i+j <= len(board):
                diagonal_line.append(board[j][i+j])
        diagonal_lines.append(diagonal_line)
    
    for i in range(1, len(board[0])-3):
        diagonal_line = []
        for j in range(len(board)):
            if i+j < len(board):
                diagonal_line.append(board[i+j][j])
        diagonal_lines.append(diagonal_line)

    board.reverse()
    for i in range(len(board[0])-3):
        diagonal_line = []
        for j in range(len(board)):
            if i+j <= len(board):
                diagonal_line.append(board[j][i+j])
        diagonal_lines.append(diagonal_line)

    for i in range(1, len(board[0])-3):
        diagonal_line = []
        for j in range(len(board)):
            if i+j < len(board):
                diagonal_line.append(board[i+j][j])
        diagonal_lines.append(diagonal_line)
    board.reverse()



    for i in vertical_lines:
        lines.append(i)
    for i in diagonal_lines:
        lines.append(i)


    return lines


def test_sequence(sequence, listtotest):

    if len(sequence) <= len(listtotest):
        return ', '.join(map(str, sequence)) in ', '.join(map(str, listtotest))
    else:
        return False


criteria = [
    [1, 1, 1, 1],
    [2, 2, 2, 2],
    [0, 1, 1, 1, 0],
    [0, 2, 2, 2, 0],
    [0, 1, 1, 1],
    [0, 2, 2, 2],
    [1, 1, 1, 0],
    [2, 2, 2, 0],
    [1, 0, 1, 1],
    [2, 0, 2, 2],
    [1, 1, 0, 1],
    [2, 2, 0, 2],
    [0, 1, 1, 0],
    [0, 2, 2, 0],
    [0, 1, 0],
]

points = [
    100000000000,
    -100000000000,
    1000,
    -10000,
    100,
    -10000,
    100,
    -10000,
    100,
    -10000,
    100,
    -10000,
    10,
    -10,
    1,
    2,
]


def get_fittness_a(board):
    global criteria, points

    lines = get_lines(board)
    score = 0
    for i, seq in enumerate(criteria):
        for line in lines:
            if test_sequence(seq, line):
                score += points[i]
    # print_board(board)
    # print("score", score)
    return score



criterium = [
    [1, 1, 1, 1],
    [2, 2, 2, 2],
]


def get_finished(board):
    global criterium
    lines = get_lines(board)
    for seq in criterium:
        for line in lines:
            if test_sequence(seq, line):
                return False

    return True


def get_move_a(board, player, level):
    scores = []
    for i in range(len(board[0])):
        if board[0][i] == 0:
            if level < 2:
                if get_finished(board.copy()):
                    if player == 1:
                        scores.append(get_move_a(drop_a([i.copy() for i in board], i), 2, level+1))
                    if player == 2:
                        scores.append(get_move_a(drop_b([i.copy() for i in board], i), 1, level+1))
                else:
                    return get_fittness_a(board)
            else:
                return get_fittness_a(board)
        else:
            return get_fittness_a(board)
    if player == 1:
        return max(scores)
    if player == 2:
        return min(scores)



def play_a(board, level):
    scores = []
    for i in tqdm(range(len(board[0]))):
        if board[0][i] == 0:
            scores.append(get_move_a(drop_a([i.copy() for i in board], i), 2, level+1))
        else:
            scores.append(-100000000000)
    print(scores)
    return scores.index(max(scores))
    


print(play_a(board, 0))

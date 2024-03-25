board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find
    
    for i in range(1,10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            if solve(bo):
                return True
            bo[row][col] = 0

    return False


def print_board(bo):
    print ("\n")
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            # print("- - - - - - - - - - - - -")
            print("- - - - - - - - - - -")
        for j in range(len(bo[0])):
            # if j % 3 == 0:
            if j % 3 == 0 and j != 0:
                print("| ",end="")

            if j == 8:
                # print(str(bo[i][j]) + " |", end="\n")
                print(bo[i][j], end="\n")
            else:
                print(str(bo[i][j]) + " ", end="")
    print ("\n")

def find_empty(bo):
    for i in range(len(bo)):
        for j in range (len(bo[0])):
            if bo[i][j] == 0:
                return (i, j) # (row, column) format
    return None

def valid(bo, num, pos):
    # check row
    for i in range(len(bo)):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # check square
    box_x = pos[1] // 3 #0, 1, or 2
    box_y = pos[0] // 3 #0, 1, or 2

    for i in range(box_y * 3, box_y * 3 + 3): #0 to 2, 3 to 5, or 6 to 8 (range is non-inclusive)
        for j in range(box_x * 3, box_x * 3 + 3): #0 to 2, 3 to 5, or 6 to 8 (range is non-inclusive)
            if bo[i][j] == num and (i,j) != pos:
                return False
    
    return True

def randomize_solvable_board(bo):
    # solve blank board, but shuffle numbers instead of going sequentially
    # then set random squares to 0 (needs to be at least 17 hints?)
    # check number of solutions?
    solvable = False
    while not solvable:
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                bo[i][j] = i
        bo_copy = bo
        if solve(bo_copy):
            solvable = True

print_board(board)
# print (find_empty(board))
solve(board)
# print_board(board)
# randomize_solvable_board(board)
print_board(board)

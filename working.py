import numpy
import random
import os
import re
from pdfminer.high_level import extract_pages, extract_text
import tabula
from pypdf import PdfReader
import pdfplumber
import copy

# 60_Sudokus_Pattern_Easy.pdf
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
solutions = []
boards = []
path = os.path.join(os.getcwd(), "boards", "60_Sudokus_Pattern_Easy.pdf")

def solve(bo,randomize=False):
    count = 0
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find
    
    num_list = numpy.array(range(1,10))
    if randomize:
        random.shuffle(num_list)
    # print(num_list)
    for i in num_list:
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            # s = solve(bo,randomize=randomize)
            if solve(bo,randomize=randomize):
                count += 1
                solutions.append(bo) if bo not in solutions else solutions
                # print(bo)
                # print(count)
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
    # solves = 10
    # for k in range(solves):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            bo[i][j] = 0
    # print_board(bo)
    solve(bo, randomize=True)
    print_board(bo)

def randomize_board(bo):
    # swap rows in block
    moves = random.randint(5,50)
    for _ in range(moves):
        rows = random.sample(range(3),2)
        # print(rows)
        temp = bo[rows[0]]
        bo[rows[0]] = bo[rows[1]]
        bo[rows[1]] = temp

    # swap rows of blocks
    moves = random.randint(5,50)
    for _ in range(moves):
        blocks = random.sample(range(3),2)
        # print(blocks)
        for i in range(3):
            swap1 = 3*blocks[0] + i
            swap2 = 3*blocks[1] + i
            temp = bo[swap1]
            bo[swap1] = bo[swap2]
            bo[swap2] = temp

    # swap columns in block
    temp_board = transform_board(bo)
    moves = random.randint(5,50)
    for _ in range(moves):
        columns = random.sample(range(3),2)
        # print(columns)
        temp = temp_board[columns[0]]
        temp_board[columns[0]] = temp_board[columns[1]]
        temp_board[columns[1]] = temp
    temp_board = transform_board(temp_board)
    bo = temp_board

    # swap columns of blocks
    temp_board = transform_board(bo)
    moves = random.randint(5,50)
    for _ in range(moves):
        blocks = random.sample(range(3),2)
        # print(blocks)
        for i in range(3):
            swap1 = 3*blocks[0] + i
            swap2 = 3*blocks[1] + i
            temp = temp_board[swap1]
            temp_board[swap1] = temp_board[swap2]
            temp_board[swap2] = temp
    temp_board = transform_board(temp_board)
    bo = temp_board

    # swap pairs of numbers
    moves = random.randint(5,50)
    for _ in range(moves):
        pair = random.sample(range(1,10),2) # pick 2 numbers 1 through 9 (not blank spaces)
        # print(pair)
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                if bo[i][j] == pair[0]:
                    bo[i][j] = pair[1]
                elif bo[i][j] == pair[1]:
                    bo[i][j] = pair[0]

    return bo

def import_board():
    pass

def transform_board(bo):
    board2 = copy.deepcopy(bo)
    for i in range(len(board2)):
        for j in range(len(board2[0])):
            board2[i][j] = 0
    for i in range(len(board2)):
        for j in range(len(board2[0])):
            board2[i][j] = bo[j][i]

    return board2


# print_board(board)
# print (find_empty(board))
# num_list = numpy.array(range(1,10))
# print(num_list)
# for i in num_list:
#     print(i)
# random.shuffle(num_list)
# print(num_list)
# for i in num_list:
#     print(i)
# print(num_list)
# solve(board)

# print_board(board)
# board = randomize_board(board)
# print_board(board)
# solve(board)
# print_board(board)

# for _ in range(10000):
#     board2 = copy.deepcopy(board)
#     board2 = randomize_board(board2)
#     solve(board2)

with pdfplumber.open(path) as f:
    for page in f.pages:
        # print(len(page.extract_tables()))
        for table in page.extract_tables():
            for i in range(len(table)):
                for j in range(len(table[0])):
                    if table[i][j] == '':
                        table[i][j] = 0
                    else:
                        table[i][j] = int(table[i][j])
            boards.append(table)
random_board = random.choice(boards)
print_board(random_board)
random_board = randomize_board(random_board)
print_board(random_board)
solve(board)
print_board(board)



    #loop through all pages (f.pages)
    #loop through all tables ([0+i:0+i+9])
        # print(page.extract_tables())
    #print each table after conversion
    # page = f.pages[0]
    # table = page.extract_table()[0:9]
    # for i in range(9):
    #     for j in range(9):
    #         if table[i][j] == '':
    #             table[i][j] = 0
    #         else:
    #             table[i][j] = int(table[i][j])
    # print_board(table)
    # solve(table,randomize=False)
    # print_board(table)
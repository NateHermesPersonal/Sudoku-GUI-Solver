import numpy
import random
import os
import re
from pdfminer.high_level import extract_pages, extract_text
import tabula
from pypdf import PdfReader
import pdfplumber

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
    temp = bo[0]
    bo[0] = bo[1]
    bo[1] = temp

    # swap rows of blocks

    # swap columns in block

    # swap columns of blocks

    # swap pairs of numbers

def import_board():
    pass

# print_board(board)
# print (find_empty(board))
# num_list = numpy.array(range(1,10))
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
# randomize_board(board)
# print_board(board)
# solve(board,randomize=False)
# print_board(board)
# print(len(solutions))
# solves = 1
# for k in range(solves):
#     randomize_solvable_board(board)
# print_board(board)

# for b in solutions:
#     print_board(b)

# print(os.getcwd())

path = os.path.join(os.getcwd(), "boards", "60_Sudokus_Pattern_Easy.pdf")

# data_frames = tabula.read_pdf(path, pages=1)
# print(data_frames[0])

# for page in extract_pages(path):
#     for element in page:
#         print(element)

# reader = PdfReader(path)
# print(len(reader.pages))
# page = reader.pages[0]
# print(page.extract_text())

with pdfplumber.open(path) as f:
    page = f.pages[0]
    table = page.extract_table()[0:9]
    print(table)
    for i in range(9):
        for j in range(9):
            if table[i][j] == '':
                table[i][j] = 0
            else:
                table[i][j] = int(table[i][j])
    print(table)
    print_board(table)
        # print(i.extract_tables())
# text = extract_text(path,page_numbers={9})
# print(text)
from copy import copy
from time import time
import sys
import threading

from problems import problems
from sudoku import print_sudoku

# global
clear_flag = 0
answer = None
cnt = 0

def get_block_by_block_number(block_num, block_type):
    if block_type == "row":
        return [block_num * 9 + i for i in range(9) ]
    elif block_type == "column":
        return [block_num + 9 * i for i in range(9)]
    else:
        head = block_num // 3 * 27 + block_num % 3 * 3
        return [head + 9 * i + j for i in range(3) for j in range(3)]

def search(sudoku):

    global clear_flag
    global answer
    global cnt

    if clear_flag:
        return
    if not valid(sudoku):
        return
    if clear(sudoku):
        answer = sudoku
        clear_flag = 1
        return

    i = 0
    while True:
        if sudoku[i] == 0:
            break
        i += 1
    
    cnt += 1
    temp_sudoku = copy(sudoku)
    for j in range(9):
        temp_sudoku[i] = j + 1
        next_search = threading.Thread(target=search, args=(temp_sudoku,))
        next_search.start()
    
def valid(sudoku):
    for block_type in ["row", "column", "block"]:
        for block_num in range(9):
            if not valid_check(sudoku, block_num, block_type):
                return False
    return True

def valid_check(sudoku, block_num, block_type):
    check_list = get_block_by_block_number(block_num, block_type)
    for i in check_list:
        for j in check_list:
            if i != j and sudoku[i] != 0 and sudoku[i] == sudoku[j]:
                return False
    return True

def clear(sudoku):
    for num in sudoku:
        if num == 0:
            return False
    if not valid(sudoku):
        return False
    return True

def main(source):
    # Too many threading won't work...
    global cnt
    global answer
    sudoku = [int(char) for char in source]
    print("Problem:")
    print_sudoku(sudoku)
    try:
        start = time()
        search(sudoku)
        cnt_line = 0
        while True:
            if cnt > cnt_line:
                print(f"Trial: {cnt}\r", end="")
                cnt_line += 100
            if answer:
                end = time()
                print("\nSolved!")
                print_sudoku(answer)
                print(f"Trial(= number of threads): {cnt}")
                print(f"Time: {end - start:.1f} sec")
                break
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prob_num = int(sys.argv[1])
    else:
        prob_num = 1
    source = problems[prob_num - 1]
    main(source)
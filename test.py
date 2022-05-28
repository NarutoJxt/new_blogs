def isValidSudoku(board) -> bool:
    for i in range(9):
        column_list = []
        row_list = []
        array_list = [[[] for i in range(3)] for j in range(3)]
        for j in range(9):
            if board[i][j] in row_list:
                return False
            else:
                if board[i][j] != ".":
                    row_list.append(board[i][j])
            if board[j][i] in column_list:
                return False
            else:
                if board[j][i] != ".":
                    column_list.append(board[j][i])
            row_index = i // 3
            col_index = j // 3
            if board[i][j] in array_list[row_index][col_index]:
                return False
            else:
                if board[i][j] != ".":
                    array_list[row_index][col_index].append(board[i][j])
    return True

a = [[".",".",".",".","5",".",".","1","."],[".","4",".","3",".",".",".",".","."],[".",".",".",".",".","3",".",".","1"],["8",".",".",".",".",".",".","2","."],[".",".","2",".","7",".",".",".","."],[".","1","5",".",".",".",".",".","."],[".",".",".",".",".","2",".",".","."],[".","2",".","9",".",".",".",".","."],[".",".","4",".",".",".",".",".","."]]
res = isValidSudoku(a)
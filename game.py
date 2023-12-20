import numpy as np


grid = np.zeros((6, 7), dtype=np.int32)
column = 1

while column != -1:
    column = int(input("Enter a column: "))
    token_placed = False
    i = grid.shape[0] - 1
    while not token_placed and i >= 0:
        current_position = grid[i, column]
        if current_position == 0:
            grid[i, column] = 1
            token_placed = True
        i -= 1
    if not token_placed:
        print("Column full!")

    print(grid)

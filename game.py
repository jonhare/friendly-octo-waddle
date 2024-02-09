import numpy as np


# grid = np.zeros((6, 7), dtype=np.int32)
# column = 1
#
# while column != -1:
#     column = int(input("Enter a column: "))
#     token_placed = False
#     i = grid.shape[0] - 1
#     while not token_placed and i >= 0:
#         current_position = grid[i, column]
#         if current_position == 0:
#             grid[i, column] = 1
#             token_placed = True
#         i -= 1
#     if not token_placed:
#         print("Column full!")
#
#     print(grid)


class Game:
    def __init__(self, shape=(6, 7), n_connect=4):
        self.board = np.zeros(shape, dtype=np.int32)
        self.n_connect = n_connect

    def check_left_right(self, r, c):
        counter = 1

        width = self.board.shape[1]

        for k in range(1, 4):
            if c + k < width and self.board[r, c + k] == self.board[r, c]:
                counter += 1
            else:
                break
        for k in range(1, 4):
            if c - k > -1 and self.board[r, c - k] == self.board[r, c]:
                counter += 1
            else:
                break

        return counter == self.n_connect

    def check_up_down(self, r, c):
        counter = 1

        height = self.board.shape[0]

        for k in range(1, 4):
            if r + k < height and self.board[r + k, c] == self.board[r, c]:
                counter += 1
            else:
                break
        for k in range(1, 4):
            if r - k > -1 and self.board[r - k, c] == self.board[r, c]:
                counter += 1
            else:
                break

        return counter == self.n_connect

    def check_negative_diagonal(self, r, c):
        counter = 1

        width = self.board.shape[1]
        height = self.board.shape[0]

        for k in range(1, 4):
            if c + k < width and r + k < height and self.board[r + k, c + k] == self.board[r, c]:
                counter += 1
            else:
                break
        for k in range(1, 4):
            if c - k > -1 and r - k > -1 and self.board[r - k, c - k] == self.board[r, c]:
                counter += 1
            else:
                break

        return counter == self.n_connect

    def check_positive_diagonal(self, r, c):
        counter = 1

        width = self.board.shape[1]
        height = self.board.shape[0]

        for k in range(1, 4):
            if c + k < width and r - k > -1 and self.board[r - k, c + k] == self.board[r, c]:
                counter += 1
            else:
                break
        for k in range(1, 4):
            if c - k > -1 and r + k < height and self.board[r + k, c - k] == self.board[r, c]:
                counter += 1
            else:
                break

        return counter == self.n_connect
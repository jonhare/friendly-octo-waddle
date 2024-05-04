import copy

import numpy as np
import argparse
import time


class Game:
    def __init__(self, shape=(6, 7), n_connect=4):
        self.board = np.zeros(shape, dtype=np.int32)
        self.n_connect = n_connect

    def check_left_right(self, r, c):
        counter = 1

        width = self.board.shape[1]

        for k in range(1, self.n_connect):
            if c + k < width and self.board[r, c + k] == self.board[r, c]:
                counter += 1
            else:
                break
        for k in range(1, self.n_connect):
            if c - k > -1 and self.board[r, c - k] == self.board[r, c]:
                counter += 1
            else:
                break

        return counter >= self.n_connect

    def check_up_down(self, r, c):
        counter = 1

        height = self.board.shape[0]

        for k in range(1, self.n_connect):
            if r + k < height and self.board[r + k, c] == self.board[r, c]:
                counter += 1
            else:
                break
        for k in range(1, self.n_connect):
            if r - k > -1 and self.board[r - k, c] == self.board[r, c]:
                counter += 1
            else:
                break

        return counter >= self.n_connect

    def check_negative_diagonal(self, r, c):
        counter = 1

        width = self.board.shape[1]
        height = self.board.shape[0]

        for k in range(1, self.n_connect):
            if c + k < width and r + k < height and self.board[r + k, c + k] == self.board[r, c]:
                counter += 1
            else:
                break
        for k in range(1, self.n_connect):
            if c - k > -1 and r - k > -1 and self.board[r - k, c - k] == self.board[r, c]:
                counter += 1
            else:
                break

        return counter >= self.n_connect

    def check_positive_diagonal(self, r, c):
        counter = 1

        width = self.board.shape[1]
        height = self.board.shape[0]

        for k in range(1, self.n_connect):
            if c + k < width and r - k > -1 and self.board[r - k, c + k] == self.board[r, c]:
                counter += 1
            else:
                break
        for k in range(1, self.n_connect):
            if c - k > -1 and r + k < height and self.board[r + k, c - k] == self.board[r, c]:
                counter += 1
            else:
                break

        return counter >= self.n_connect

    def check_all(self, r, c):
        return (self.check_positive_diagonal(r, c)
                or self.check_negative_diagonal(r, c)
                or self.check_up_down(r, c)
                or self.check_left_right(r, c))

    def add_piece(self, c, p):
        """
        Add a piece to column c and return the row. And return -1 if the column is full or the column is out of bounds.
        """
        if c < 0 or c >= self.board.shape[1]:
            return -1
        counter = self.board.shape[0] - 1

        while counter >= 0 and self.board[counter, c] != 0:
            counter -= 1

        if counter != -1:
            self.board[counter, c] = p

        return counter

    def check_draw(self):
        return (self.board[0] != 0).all()

    def __repr__(self):
        printed_board = ""
        rows, columns = self.board.shape

        printed_board += "| "
        for c in range(columns):
            printed_board += str(c) + " "
        printed_board += "|\n"

        for r in range(rows):
            printed_board += "| "
            for c in range(columns):
                if self.board[r][c] == 0:
                    printed_board += "  "
                else:
                    printed_board += str(self.board[r][c]) + " "
            printed_board += "|\n"

        return printed_board


class Player:
    def __init__(self, id):
        self.id = id

    def move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, id):
        super().__init__(id)

    def move(self, game):
        move = get_human_input(f"Player {self.id} select your column ")
        while r := game.add_piece(move, self.id):
            if r != -1:
                break
            move = get_human_input(f"Invalid Move - Player {p} select your column ")
        return move, r


class RandomPlayer(Player):
    """Completely random player"""
    def __init__(self, id):
        super().__init__(id)

    def move(self, game):
        move = np.random.randint(0, game.board.shape[1])
        while r := game.add_piece(move, self.id):
            if r != -1:
                break
            move = np.random.randint(0, game.board.shape[1])
        # time.sleep(1)
        return move, r


class LookaheadPlayer(RandomPlayer):
    """Random player that looks-ahead for a winning or blocking move"""
    def __init__(self, id):
        super().__init__(id)

    def winning_move(self, game):
        for c in range(game.board.shape[1]):
            game_copy = copy.deepcopy(game)
            r = game_copy.add_piece(c, self.id)
            if r != -1:
                if game_copy.check_all(r, c):
                    return c
        return -1

    def blocking_move(self, game):
        # search all possible moves for the other player to see if they can
        # make one that will win. If we find one, we occupy that place on the
        # board instead
        for c in range(game.board.shape[1]):
            game_copy = copy.deepcopy(game)
            other_id = 2 if self.id == 1 else 1  # TODO: handle more than two players
            r = game_copy.add_piece(c, other_id)
            if r != -1:
                if game_copy.check_all(r, c):
                    return c
        return -1

    def move(self, game):
        # check if we can win from the current state
        move = self.winning_move(game)
        if move != -1:
            return move, game.add_piece(move, self.id)

        # check if we can block the other player from winning
        move = self.blocking_move(game)
        if move != -1:
            return move, game.add_piece(move, self.id)

        # otherwise choose randomly
        return super().move(game)


def norm(arr):
    return arr #TODO: create normalisation function


class IntelligentPlayer(Player):

    def __init__(self, id):
        super().__init__()
        self.id = id
        self.qtable = dict()
        self.sample = False

    def move(self, game):
        current_state = game.board.tostring()
        if self.sample:
            np.random.choice(list(range(game.board.shape[1])), p=norm(self.qtable[current_state]))
        else:
            move = self.qtable[current_state].argmax()
        while r := game.add_piece(move, self.id):
            if r != -1:
                break
            move = np.random.randint(0, game.board.shape[1])
        time.sleep(1)
        return move, r



def get_human_input(prompt):
    while True:
        raw = input(prompt)
        if raw.isnumeric():
            return int(raw)
        print("Invalid input")


def create_player(type, id):
    type = type.capitalize() + "Player"
    return globals()[type](id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Connect-4 Game')
    parser.add_argument('--nrows', type=int, default=6)
    parser.add_argument('--ncols', type=int, default=7)
    parser.add_argument('--nconnect', type=int, default=4)
    parser.add_argument('--player1', type=str, default="human")
    parser.add_argument('--player2', type=str, default="random")
    parser.add_argument('--num-games', type=int, default=1)
    flags = parser.parse_args()

    game_stats = {'player1': 0, 'player2': 0, 'draw': 0}
    for g in range(flags.num_games):
        game = Game(shape=(flags.nrows, flags.ncols), n_connect=flags.nconnect)
        players = [create_player(flags.player1, 1), create_player(flags.player2, 2)]

        p = 1
        print(game)
        while True:
            move, r = players[p - 1].move(game)

            print(game)
            if game.check_all(r, move):
                print(f"Player {p} wins!")
                game_stats[f'player{p}'] += 1
                break

            if game.check_draw():
                print("Draw has been reached")
                game_stats['draw'] += 1
                break

            p = 2 if p == 1 else 1

    print(game_stats)
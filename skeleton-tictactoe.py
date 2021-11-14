# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

from random import randint
import numpy as np
import time


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3
    N = 4
    S = 3
    B = 2

    def __init__(self, recommend=True, blocksLocations=None):
        self.initialize_game(blocksLocations)
        self.recommend = recommend

    def initialize_game(self, blocksLocations=None):
        self.current_state = np.full((self.N,self.N), '.')

        if (blocksLocations == None):
            self.randomBlocks()
        else:
            self.insertBlocks(blocksLocations)

        # Player X always plays first
        self.player_turn = 'X'
        
    # inserts b randome blocks
    def randomBlocks(self):
        for i in range(0, self.B):
            x = randint(0, self.N - 1)
            y = randint(0, self.N - 1)
            while (self.current_state[x][y] != '.'):
                x = randint(0, self.N - 1)
                y = randint(0, self.N - 1)
            self.current_state[x][y] = '#'

    # inserts given blocks on their coordinates
    def insertBlocks(self, blocksLocations):
        for i in blocksLocations:
            self.current_state[i[0]][i[1]] = '#'

    def draw_board(self):
        print()
        for y in range(0, self.N):
            for x in range(0, self.N):
                print(F'{self.current_state[x][y]}', end=" ")
            print()
        print()


    # counts the number of the given symbol on a line
    def symbolCount(self, line, symbol):
        counter = 0
        for char in line:
            if char == symbol:
                counter += 1
        return counter


    # Determines if there's a win on a line
    def checkWin(self, line):
        if max(self.consecutiveCount(line,'X')) >= self.S:
            return 'X'
        if max(self.consecutiveCount(line,'O')) >= self.S:
            return 'O'
        return '.'

    # checkWin's helper function. Outputs a list with the count of consecutive of given symbol
    def consecutiveCount(self, line, symbol):
        previous = "-"
        counter = 0
        consecutiveList = []
        for char in line:
            if char == symbol:
                if previous == symbol:
                    if counter == 0:
                        counter = 1
                    counter += 1
                else:
                    if counter != 0:
                        consecutiveList.append(counter)
                    counter = 0
            previous = char
            consecutiveList.append(counter)
        return consecutiveList

    def is_end(self):
        # vertical - checking each vertical line for a win
        for x in range(0, self.N):
            symbol = self.checkWin(self.current_state[:,x])
            if (symbol != '.'):
                return symbol

        # horizontal - checking each horizontal line for a win
        for x in range(0, self.N):
            symbol = self.checkWin(self.current_state[x])
            if (symbol != '.'):
                return symbol

        # diagonal - checking each diagonal line for a win
        for x in range(-self.N + 1, self.N):
            symbol = self.checkWin(self.current_state.diagonal(x))
            if (symbol != '.'):
                return symbol

        # diagonalInverted - checking each inverted diagonal line for a win
        for x in range(-self.N + 1, self.N):
            symbol = self.checkWin(np.flipud(self.current_state).diagonal(x))
            if (symbol != '.'):
                return symbol

        # Is whole board full?
        for i in range(0, self.N):
            for j in range(0, self.N):
                # There's an empty field, we continue the game
                if (self.current_state[i][j] == '.'):
                    return None
        return '.'

    def is_valid(self, px, py):
        if px < 0 or px > self.N-1 or py < 0 or py > self.N-1:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == 'X':
                print('The winner is X!')
            elif self.result == 'O':
                print('The winner is O!')
            elif self.result == '.':
                print("It's a tie!")
            self.initialize_game()
        return self.result

    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            px = int(input('enter the x coordinate: '))
            py = int(input('enter the y coordinate: '))
            if self.is_valid(px, py):
                return (px, py)
            else:
                print('The move is not valid! Try again.')

    def switch_player(self):
        if self.player_turn == 'X':
            self.player_turn = 'O'
        elif self.player_turn == 'O':
            self.player_turn = 'X'
        return self.player_turn

    # goes through every line and counts the number of Xs and Ys and gives a h(n).
    # A higher h(n) is better for X.
    def heuristicSimple(self):
        total = 0

        print("verticals")
        for x in range(0, self.N):
            xCount = self.symbolCount(self.current_state[:, x], "X")
            yCount = self.symbolCount(self.current_state[:, x], "O")
            total += self.valueAttributor(xCount, yCount)
        print()

        print()
        print("horrizontals")
        for x in range(0, self.N):
            xCount = self.symbolCount(self.current_state[x], "X")
            yCount = self.symbolCount(self.current_state[x], "O")
            total += self.valueAttributor(xCount, yCount)
            print()

        print("diagonal1")
        for x in range(-self.N + 1, self.N):
            xCount = self.symbolCount(self.current_state.diagonal(x), "X")
            yCount = self.symbolCount(self.current_state.diagonal(x), "O")
            total += self.valueAttributor(xCount, yCount)
            print()

        print("diagonal2")
        for x in range(-self.N + 1, self.N):
            xCount = self.symbolCount(np.flipud(self.current_state).diagonal(x), "X")
            yCount = self.symbolCount(np.flipud(self.current_state).diagonal(x), "O")
            total += self.valueAttributor(xCount, yCount)
            print()

        print(total)

    # heuristicSimple's helper function. Gives the value of the heuristic based on the count of X and Y
    def valueAttributor(self, countX, countO):
        value = 0
        if countO == 0 and countX == 0:
            return 0
        if countO > countX:
            value = - pow(10, countO)
        else:
            value = pow(10, countX)
        return value

    def minimax(self, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            return (-1, x, y)
        elif result == 'O':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        for i in range(0, self.N):
            for j in range(0, self.N):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.minimax(max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.minimax(max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return (value, x, y)

    def alphabeta(self, alpha=-2, beta=2, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            return (-1, x, y)
        elif result == 'O':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        for i in range(0, self.N):
            for j in range(0, self.N):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.alphabeta(alpha, beta, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.alphabeta(alpha, beta, max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
                    if max:
                        if value >= beta:
                            return (value, x, y)
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return (value, x, y)
                        if value < beta:
                            beta = value
        return (value, x, y)

    def play(self, algo=None, player_x=None, player_o=None):
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        while True:
            self.draw_board()
            if self.check_end():
                return
            start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(max=False)
                else:
                    (_, x, y) = self.minimax(max=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(max=False)
                else:
                    (m, x, y) = self.alphabeta(max=True)
            end = time.time()
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            self.current_state[x][y] = self.player_turn
            self.switch_player()


def main():
    g = Game(recommend=True)
    g.play(algo=Game.ALPHABETA, player_x=Game.AI, player_o=Game.AI)
    g.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.HUMAN)


if __name__ == "__main__":
    main()
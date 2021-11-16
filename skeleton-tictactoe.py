# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python
#test123

from math import inf
from random import randint
import numpy as np
import time


class Game:
roundCounter = 0
    HUMAN = 2
    AI = 3
    MINIMAX = 0
    ALPHABETA = 1

    def getAlphaMin(self):
        while True:
            try:
                max = input('Enter True to use alphabeta or False to use minmax: ')
                if max == "True":
                    max = True
                    break
                if max == "False":
                    max = False
                    break
                if max != True or max != False:
                    raise ValueError
                break
            except ValueError:
                print("Please Enter Valid Entry")

    def getT(self):
        t = 0
        while True:
            try:
                t = int(input('Enter t: '))
                if t < 0:
                    raise ValueError
                break
            except ValueError:
                print("Please Enter Valid t")
    def getN(self):
        N = 3
        while True:
            try:
                N = int(input('Enter N(3..10): '))
                if N < 3 or N > 10:
                    raise ValueError
                break
            except ValueError:
                print("Please Enter Valid Number")
    def getB(self):
        B = 3
        while True:
            try:
                B = int(input('Enter B (3..n): '))
                if B < 3:
                    raise ValueError
                break
            except ValueError:
                print("Please Enter Valid Number")

    def getS(self):
        S = 0
        while True:
            try:
                S = int(input('Enter S(0..n): '))
                if S < 0:
                    raise ValueError
                break
            except ValueError:
                print("Please Enter Valid Number")

    def getPlayerX(self):
        player_x = 0
        while True:
            try:
                player_x = int(input('Player_x Enter 1 for AI or 0 for Human: '))
                if player_x < 0 or player_x > 1:
                    raise ValueError
                break
            except ValueError:
                print("Please Enter Valid Entry")

    def getPlayerO(self):
        player_o = 0
        while True:
            try:
                player_o = int(input('Player_o Enter 1 for AI or 0 for Human: '))
                if player_o < 0 or player_o > 1:
                    raise ValueError
                break
            except ValueError:
                print("Please Enter Valid Entry")

    print("n:" + str(N) + " b: " + str(B) + " s: " + str(S) + " t: " + str(t))

    player = 0
    d1 = 1
    d2 = 1
    e = 1

    print("Player 1: human" if player == 1 else "Player 1: AI d= " +
          str(d1) + " a= " + str(max) + " e1= " + str(e))               # TO BE DONE

    print("Player 2: human" if player == 1 else "Player 2: AI d= " +
          str(d2) + " a= " + str(max) + " e2= " + str(e))



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

    # inserts b random blocks

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

    # helper that checks for consecutive symbols including "."
    def consecutivePlus(self, line, symbol):
        previous = "-"
        counter = 0
        consecutiveList = []
        for char in line:
            if char == symbol or ".":
                if previous == symbol or ".":
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

    def heuristicOther(self):
        total = 0

        for x in range(0, self.N):
            xCount = self.symbolCount(self.current_state[:, x], "X")
            yCount = self.symbolCount(self.current_state[:, x], "O")
            total += self.valueAttributor(xCount, yCount)

        for x in range(0, self.N):
            xCount = self.symbolCount(self.current_state[x], "X")
            yCount = self.symbolCount(self.current_state[x], "O")
            total += self.valueAttributor(xCount, yCount)

        for x in range(-self.N + 1, self.N):
            xCount = self.symbolCount(self.current_state.diagonal(x), "X")
            yCount = self.symbolCount(self.current_state.diagonal(x), "O")
            total += self.valueAttributor(xCount, yCount)

        for x in range(-self.N + 1, self.N):
            xCount = self.symbolCount(np.flipud(self.current_state).diagonal(x), "X")
            yCount = self.symbolCount(np.flipud(self.current_state).diagonal(x), "O")
            total += self.valueAttributor(xCount, yCount)

        return total

    # goes through every line and counts the number of Xs and Ys and gives a h(n).
    # A higher h(n) is better for X.
    def heuristicSimple(self):
        total = 0

        for x in range(0, self.N):
            xCount = self.symbolCount(self.current_state[:, x], "X")
            yCount = self.symbolCount(self.current_state[:, x], "O")
            total += self.valueAttributor(xCount, yCount)

        for x in range(0, self.N):
            xCount = self.symbolCount(self.current_state[x], "X")
            yCount = self.symbolCount(self.current_state[x], "O")
            total += self.valueAttributor(xCount, yCount)

        for x in range(-self.N + 1, self.N):
            xCount = self.symbolCount(self.current_state.diagonal(x), "X")
            yCount = self.symbolCount(self.current_state.diagonal(x), "O")
            total += self.valueAttributor(xCount, yCount)

        for x in range(-self.N + 1, self.N):
            xCount = self.symbolCount(np.flipud(self.current_state).diagonal(x), "X")
            yCount = self.symbolCount(np.flipud(self.current_state).diagonal(x), "O")
            total += self.valueAttributor(xCount, yCount)

        return total

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

    def minimax(self, d1, d2, max=False, heuristic=False):
        value = 999999999
        if max:
            value = -999999999
        x = None
        y = None
        result = self.is_end()

        if heuristic == True:
            if result == 'X':
                return (-1, x, y)
            elif result == 'O':
                return (1, x, y)
            elif result == '.':
                return (0, x, y)
            elif d1 == 0:
                return (self.heuristicSimple(), x, y)
            elif d2 == 0:
                return (self.heuristicSimple(), x, y)
        else:
            if result == 'X':
                return (-1, x, y)
            elif result == 'O':
                return (1, x, y)
            elif result == '.':
                return (0, x, y)
            elif d1 == 0:
                return (self.heuristicSimple(), x, y)
            elif d2 == 0:
                return (self.heuristicSimple(), x, y)

        for i in range(0, self.N):
            for j in range(0, self.N):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.minimax(d1, d2-1, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.minimax(d1-1, d2, max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return (value, x, y)

    # the recursive call is (depth -1)
    # when either of the base cases are reached before a win is determined (d1,d2 == 0) we return the (heuristic,x,y)
    def alphabeta(self, d1, d2, alpha=-2, beta=2, max=False, heuristic=False):

        value = 999999999
        if max:
            value = -999999999
        x = None
        y = None
        result = self.is_end()

        if heuristic == True:
            if result == 'X':
                return (-1, x, y)
            elif result == 'O':
                return (1, x, y)
            elif result == '.':
                return (0, x, y)
            elif d1 == 0:
                return (self.heuristicSimple(), x, y)
            elif d2 == 0:
                return (self.heuristicSimple(), x, y)
        else:
            if result == 'X':
                return (-1, x, y)
            elif result == 'O':
                return (1, x, y)
            elif result == '.':
                return (0, x, y)
            elif d1 == 0:
                return (self.heuristicSimple(), x, y)
            elif d2 == 0:
                return (self.heuristicSimple(), x, y)

        for i in range(0, self.N):
            for j in range(0, self.N):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.alphabeta(d1, d2-1, alpha, beta, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.alphabeta(d1-1, d2, alpha, beta, max=True)
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
        #depth for d1 is the X player, d2 is the O player
        d1=2
        d2=9
        heuris = True
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
                    (_, x, y) = self.minimax(d1, d2, max=False)
                    if self.t <= (time.time() - start):
                      print("Player O wins because Player X took too long")
                      exit()
                else:
                    (_, x, y) = self.minimax(d1, d2, max=True)
                    if self.t <= (time.time() - start):
                      print("Player X wins because Player O took too long")
                      exit()
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(d1, d2, max=False)
                    if self.t <= (time.time() - start):
                      print("Player O wins because Player X took too long")
                      exit()
                else:
                    (m, x, y) = self.alphabeta(d1, d2, max=True)
                    if self.t <= (time.time() - start):
                      print("Player X wins because Player O took too long")
                      exit()
            end = time.time()
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                  print('Round ' + str(self.roundCounter))
                  print(F'Evaluation time: {round(end - start, 7)}s')
                  print(F'Recommended move: x = {x}, y = {y}')
                  self.roundCounter += 1
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                print('Round ' + str(self.roundCounter))
                self.roundCounter += 1
                print(F'Evaluation time: {round(end - start, 7)}s')
                # print('ii Total heuristic evaluations: ' + str(HE))
                # print('iii Evaluations by depth: {' + str(Ed) + '}')
                # print('iv  Average evaluation depth: ' + str(AEd))
                # print('v Average recursion depth:' + str(ARd))
                # print('vi  Average moves per game: ' + str(Ampg))
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            self.current_state[x][y] = self.player_turn
            self.switch_player()

def main():
    g = Game(recommend=True)
    g.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.AI)

if __name__ == "__main__":
    main()

def print(self):     
    file = open("gameTrace-" + str(self.N) + str(self.B) + str(self.S) + str(self.t)+ ".txt", 'w')
    sys.stdout = file
    file.close()


# boilterplate for Test Stats

#def TestPrint(self):
# print("n:" +str(N)+ " b: " +str(B)+ " s: " +str(S)+ " t: " +str(t))

# print("Player 1: d= " + str(d1) + " a= " + str(max))

# print("Player 2: d= " + str(d2) + " a= " + str(max))

# print(str(Totalgames) + "games")

# print("Total wins for heuristic e1: " + str(WinsE1) + " (" + str(WinsE1/Totalgames * 100) + "%) " + e  )
# print("Total wins for heuristic e2: " + str(WinsE2) + " (" + str(WinsE2/Totalgames * 100) + "%) " + e  )

# print('i Average evaluation time: ' + str(Aet))
# print('ii Total heuristic evaluations: ' + str(HE))
# print('iii Evaluations by depth: {' + str(Ed) + '}')
# print('iv  Average evaluation depth: ' + str(AEd))
# print('v Average recursion depth:' + str(ARd))
# print('vi  Average moves per game: ' + str(Ampg))

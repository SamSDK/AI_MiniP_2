# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python
#test123

from math import inf
from random import randint
import numpy as np
import time
import sys


class Game:
    roundCounter = 0
    HUMAN = 2
    AI = 3
    MINIMAX = 0
    ALPHABETA = 1



    def __init__(self, blocksLocations=None, recommend=True):
        self.recommend = recommend
        self.playerXscore = 0
        self.playerOscore = 0
        self.heuristicCounter = 0
        self.roundCounterTotal = 0

        self.nbOfGame = self.setNbOfGames()
        self.max = self.getAlphaMin()
        self.t = self.setT()
        self.N = self.setN()
        self.B = self.setB()
        self.S = self.setS()
        self.player_x = self.setPlayerX()
        self.player_o = self.setPlayerO()
        self.player_x_heurstic = self.setPlayerXHeuristic
        self.player_O_heurstic = self.setPlayerOHeuristic
        self.player_x_depth = self.setPlayerXDepth
        self.player_o_depth = self.setPlayerODepth

        self.initialize_game(blocksLocations)

        self.file = open("gameTrace-" + str(self.N) + str(self.B) + str(self.S) + str(self.t) + ".txt", 'w')
        sys.stdout = self.file
        print("\nn:" + str(self.N) + " b: " + str(self.B) + " s: " + str(self.S) + " t: " + str(self.t))

        for i in range (0,self.nbOfGame):
            self.play()

        self.outputStats()

    def setNbOfGames(self):
        nbOfGame = 0
        while True:
            try:
                nbOfGame = int(input('Enter number of games you want to play (1..n): '))
                if nbOfGame < 1:
                    raise ValueError
                break
            except ValueError:
                print("Please Enter Valid Number")
        return nbOfGame

    def insertBlocksManually(self):
        choice = "no"
        while True:
            try:
                choice = input('Do you wish to choose the location of the n blocks ? (Yes or No)\n')
                if choice.lower() == "yes":
                    for i in range(0, self.B):
                        px = int(input('enter the x coordinate: '))
                        py = int(input('enter the y coordinate: '))
                        if self.is_valid(px, py):
                            self.current_state[px][py] = '#'
                        else:
                            print('The location is not valid! Try again.')
                    break
                if choice.lower() == "no":
                    self.randomBlocks()
                    break
                raise ValueError
            except ValueError:
                print("Please Enter Valid answer")

    def initialize_game(self, blocksLocations=None):
        self.current_state = np.full((self.N, self.N), '.')

        if (blocksLocations == None):
            self.insertBlocksManually()
        else:
            self.insertBlocks(blocksLocations)

        # Player X always plays first
        self.player_turn = 'X'


    def getAlphaMin(self):
        while True:
            try:
                max = input('Enter True to use alphabeta or False to use minmax: ')
                if max.lower() == "true":
                    max = True
                    break
                if max.lower() == "false":
                    max = False
                    break
                if max != True or max != False:
                    raise ValueError
                break
            except ValueError:
                print("Please Enter Valid Entry")
        return max

    def setT(self):
        t = 0
        while True:
            try:
                t = int(input('Enter t: '))
                if t < 0:
                    raise ValueError
                break
            except ValueError:
                print("Please Enter Valid t")
        return t

    def setN(self):
        N = 3
        while True:
            try:
                N = int(input('Enter N(3..10): '))
                if N < 3 or N > 10:
                    raise ValueError
                break
            except ValueError:
                print("Please Enter Valid Number")
        return N

    def setB(self):
        B = 3
        while True:
            try:
                B = int(input('Enter B (0..n): '))
                if B < 0:
                    raise ValueError
                break
            except ValueError:
                print("Please Enter Valid Number")
        return B

    def setS(self):
        S = 0
        while True:
            try:
                S = int(input('Enter S(3..n): '))
                if S < 3:
                    raise ValueError
                break
            except ValueError:
                print("Please Enter Valid Number")
        return S

    def setPlayerX(self):
        player_x = 0
        while True:
            try:
                player_x = int(input('Player_x Enter 1 for AI or 0 for Human: '))
                if player_x < 0 or player_x > 1:
                    raise ValueError
                if player_x == 1:
                    player_x = Game.AI
                else:
                    player_x = Game.HUMAN
                break
            except ValueError:
                print("Please Enter Valid Entry")
        return player_x

    def setPlayerO(self):
        player_o = 0
        while True:
            try:
                player_o = int(input('Player_o Enter 1 for AI or 0 for Human: '))
                if player_o < 0 or player_o > 1:
                    raise ValueError
                if player_o == 1:
                    player_o = Game.AI
                else:
                    player_o = Game.HUMAN
                break
            except ValueError:
                print("Please Enter Valid Entry")
        return player_o

    def setPlayerXHeuristic(self):
        player_x_heurstic = 0
        while True:
            try:
                heuristic = int(input('Player_x Enter 1 for the fast heuristic or 0 for longer heuristic: '))
                if heuristic < 0 or heuristic > 1:
                    raise ValueError
                if heuristic == 1:
                    player_X_heurstic = True
                else:
                    player_X_heurstic = False
                break
            except ValueError:
                print("Please Enter Valid Entry")
        return player_X_heurstic

    def setPlayerOHeuristic(self):
        player_o_heurstic = 0
        while True:
            try:
                heuristic = int(input('Player_o Enter 1 for the fast heuristic or 0 for longer heuristic: '))
                if heuristic < 0 or heuristic > 1:
                    raise ValueError
                if heuristic == 1:
                    player_o_heurstic = True
                else:
                    player_o_heurstic = False
                break
            except ValueError:
                print("Please Enter Valid Entry")
        return player_o_heurstic

    def setPlayerXDepth(self):
        player_x_depth = 0
        while True:
            try:
                S = int(input('Enter the maximum depth for player X (0..n): '))
                if S < 0:
                    raise ValueError
                break
            except ValueError:
                print("Please Enter Valid Number")
        return player_x_depth

    def setPlayerODepth(self):
        player_o_depth = 0
        while True:
            try:
                S = int(input('Enter the maximum depth for player O (0..n): '))
                if S < 0:
                    raise ValueError
                break
            except ValueError:
                print("Please Enter Valid Number")
        return player_o_depth

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
        counter = 0
        consecutiveList = []
        for char in line:
            if char == symbol:
                counter += 1
            else:
                consecutiveList.append(counter)
                counter = 0
        consecutiveList.append(counter)
        return consecutiveList

    # helper that checks for consecutive symbols including "."
    def consecutivePlus(self, line, symbol):
        counter = 0
        consecutiveList = []
        for char in line:
            if char == symbol or char == '.':
                counter += 1
            else:
                consecutiveList.append(counter)
                counter = 0
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

    def valueCounter(self, line):
        winningLinesX = 0
        winningLinesO = 0
        countX = self.symbolCount(line, 'X')
        countO = self.symbolCount(line, 'O')
        consecutiveWinX = self.consecutivePlus(line, 'X')
        consecutiveWinO = self.consecutivePlus(line, 'O')

        for i in consecutiveWinX:
            if (i >= self.S):
                winningLinesX += 1
        for j in consecutiveWinO:
            if (j >= self.S):
                winningLinesO += 1

        return (winningLinesX * pow(10, countX)) - (winningLinesO * pow(10, countO))

    def heuristicComplex(self):
        total = 0

        for x in range(0, self.N):
            total += self.valueCounter(self.current_state[:, x])

        for x in range(0, self.N):
            total += self.valueCounter(self.current_state[x])

        for x in range(-self.N + 1, self.N):
            total += self.valueCounter(self.current_state.diagonal(x))

        for x in range(-self.N + 1, self.N):
            total += self.valueCounter(np.flipud(self.current_state).diagonal(x))

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

    #the recursive call of the function minimax decrements the max depths we set by 1 each time it is called
    #when either of the base cases are reached (when depth 1 or depth 2 are decremented to '0') before a winner is determined
    #we use one of our heursitic functions to return the approximated value of the decision along with x and y
    #depth 2 represents the 'O' players turn while depth 1 represents the 'X' players turn 
    def minimax(self, heurstic, d1, d2, max=False):
        value = 999999999
        if max:
            value = -999999999
        x = None
        y = None
        result = self.is_end()

        if heurstic == True:
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
                return (self.heuristicComplex(), x, y)
            elif d2 == 0:
                return (self.heuristicComplex(), x, y)

        for i in range(0, self.N):
            for j in range(0, self.N):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.minimax(heurstic, d1, d2-1, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.minimax(heurstic, d1-1, d2, max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return (value, x, y)

    #the recursive call of the function alphabeta decrements the max depths we set by 1 each time it is called
    #when either of the base cases are reached (when depth 1 or depth 2 are decremented to '0') before a winner is determined
    #we use one of our heursitic functions to return the approximated value of the decision along with x and y
    #depth 2 represents the 'O' players turn while depth 1 represents the 'X' players turn 
    def alphabeta(self, heuristic, d1, d2, alpha=-2, beta=2, max=False):

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
                return (self.heuristicComplex(), x, y)
            elif d2 == 0:
                return (self.heuristicComplex(), x, y)

        for i in range(0, self.N):
            for j in range(0, self.N):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.alphabeta(heuristic, d1, d2-1, alpha, beta, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.alphabeta(heuristic, d1-1, d2, alpha, beta, max=True)
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

    def play(self):
        if self.max == True:
            algo = self.ALPHABETA
        if self.player_x == None:
            player_x = self.HUMAN
        if self.player_o == None:
            player_o = self.HUMAN
        while True:
            self.draw_board()
            if self.check_end():
                return
            start = time.time()
            if self.max == False:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax( self.player_x_heurstic, self.player_x_depth, self.player_o_depth, max=False)
                    if self.t <= (time.time() - start):
                        print("Player O wins because Player X took too long")
                        self.playerOscore += 1
                        break
                else:
                    (_, x, y) = self.minimax(self.player_o_heurstic, self.player_x_depth, self.player_o_depth, max=True)
                    if self.t <= (time.time() - start):
                        print("Player X wins because Player O took too long")
                        self.playerXscore += 1
                        break
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(self.player_x_heurstic, self.player_x_depth, self.player_o_depth, max=False)
                    if self.t <= (time.time() - start):
                        print("Player O wins because Player X took too long")
                        self.playerOscore += 1
                        break
                else:
                    (m, x, y) = self.alphabeta(self.player_o_heurstic,self.player_x_depth, self.player_o_depth, max=True)
                    if self.t <= (time.time() - start):
                        print("Player X wins because Player O took too long")
                        self.playerXscore += 1
                        break
            end = time.time()
            if (self.player_turn == 'X' and self.player_x == self.HUMAN) or (
                    self.player_turn == 'O' and self.player_o == self.HUMAN):
                if self.recommend:
                  print('Round ' + str(self.roundCounter))
                  print(F'Evaluation time: {round(end - start, 7)}s')
                  print(F'Recommended move: x = {x}, y = {y}')
                  self.roundCounter += 1
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and self.player_x == self.AI) or (self.player_turn == 'O' and self.player_o == self.AI):
                print('Round ' + str(self.roundCounter))
                self.roundCounter += 1
                self.roundCounterTotal += self.roundCounter
                print(F'Evaluation time: {round(end - start, 7)}s')

                HE = 0
                if (self.player_turn == 'X'):
                    if (self.player_x_heurstic == True):
                        HE = self.heuristicSimple()
                    else:
                        HE = self.heuristicComplex()
                else:
                    if (self.player_o_heurstic == True):
                        HE = self.heuristicSimple()
                    else:
                        HE = self.heuristicComplex()

                self.heuristicCounter += HE
                print('ii Total heuristic evaluations: ' + str(HE))

                # print('iii Evaluations by depth: {' + str(Ed) + '}')

                # print('iv  Average evaluation depth: ' + str(AEd))
                # print('v Average recursion depth:' + str(ARd))
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            self.current_state[x][y] = self.player_turn
            self.switch_player()

            self.file.close

    def outputStats(self):
        self.file2 = open("scoreboard.txt", 'w')
        sys.stdout = self.file2
        print("\nn:" + str(self.N) + " b: " + str(self.B) + " s: " + str(self.S) + " t: " + str(self.t))

        print("Player 1: d= " + str(self.player_x_depth) + " a= " + str("True" if self.max == True else "False"))
        print("Player 2: d= " + str(self.player_o_depth) + " a= " + str("True" if self.max == True else "False"))

        print(str(self.nbOfGame) + " games")

        print("Total wins for heuristic e1: " + str(self.playerXscore) + " (" + str(self.playerXscore / self.nbOfGame * 100) + "%) " + str("simple" if self.player_x_heurstic == True else "complex"))
        print("Total wins for heuristic e2: " + str(self.playerOscore) + " (" + str(self.playerOscore / self.nbOfGame * 100) + "%) " + str("simple" if self.player_o_heurstic == True else "complex"))

        # print('i Average evaluation time: ' + str(Aet))
        print('ii Total heuristic evaluations: ' + int(self.heuristicCounter))
        # print('iii Evaluations by depth: {' + str(Ed) + '}')
        # print('iv  Average evaluation depth: ' + str(AEd))
        # print('v Average recursion depth:' + str(ARd))
        print('vi  Average moves per game: ' + int(self.roundCounterTotal / self.nbOfGame))

        self.file2.close

def main():
    g = Game(recommend=True)

if __name__ == "__main__":
    main()



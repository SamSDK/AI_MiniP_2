from random import randint

import numpy as np

# game= [['O','O','X','#','X'],
#        ['X','#','X','X','O'],
#        ['#','X','.','#','O'],
#        ['O','#','X','X','O'],
#        ['X','O','#','O','O']]

game= [['O','O','.','#','X'],
       ['X','.','X','X','O'],
       ['#','X','.','#','.'],
       ['.','#','X','X','O'],
       ['X','O','#','O','O']]

# game= [['.','.','X','#','X'],
#        ['X','.','X','X','O'],
#        ['#','X','.','#','.'],
#        ['.','#','X','X','O'],
#        ['X','O','#','O','O']]
N = 5
S = 4
B = 1
a = np.array(game)
# a = np.arange(25).reshape(N,N)
# a = np.full((N,N), '.')
print(a)


def consecutiveX(line, symbol):
       previous = "-"
       counter = 0
       consecutiveList = []
       for char in line:
              if (char == symbol):
                     if (previous == symbol):
                            if (counter == 0):
                                   counter = 1
                            counter+=1
                     else:
                            if (counter != 0):
                                   consecutiveList.append(counter)
                            counter = 0
              previous = char
              consecutiveList.append(counter)
       return consecutiveList

# def consecutiveCountOri(line, symbol):
#  previous = "-"
#  counter = 0
#  consecutiveList = []
#  for char in line:
#      if char == symbol:
#          if previous == symbol:
#              if counter == 0:
#                  counter = 1
#              counter += 1
#          else:
#              if counter != 0:
#                  consecutiveList.append(counter)
#              counter = 0
#      previous = char
#      consecutiveList.append(counter)
#  return consecutiveList




# def consecutivePlusOri(line, symbol):
#        previous = "-"
#        counter = 0
#        consecutiveList = []
#        for char in line:
#               if char == symbol or char == '.':
#                      if previous == symbol or previous == '.':
#                             if counter == 0:
#                                    counter = 1
#                             counter += 1
#                      else:
#                             if counter != 0:
#                                    consecutiveList.append(counter)
#                             counter = 0
#               previous = char
#               consecutiveList.append(counter)
#        return consecutiveList

def consecutiveCount(line, symbol):
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

def consecutivePlus(line, symbol):
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

def heuristicLong(line):
       print(consecutivePlus(line, 'X'))
       print(consecutivePlus(line, 'Y'))




test = ['.','.','X','#','.','.','X','.','#','O','.','.','.','.','.','#','.',]
print(test)
print(consecutivePlus(test,'X'))
print(consecutiveCount(test, 'X'))

def symbolCount(line, symbol):
       counter = 0
       for char in line:
              if (char == symbol):
                     counter+=1
       return counter


def heuristicSimple():
       total = 0

       print("verticals")
       for x in range(0, N):
              print(a[:, x])
              xCount = symbolCount(a[:, x], "X")
              yCount = symbolCount(a[:, x], "O")
              total += valueAttributor(xCount, yCount)
       print()

       print()
       print("horrizontals")
       for x in range(0, N):
              print(a[x])
              xCount = symbolCount(a[x], "X")
              yCount = symbolCount(a[x], "O")
              total += valueAttributor(xCount, yCount)
              print()

       print("diagonal1")
       for x in range(-N + 1, N):
              print(a.diagonal(x))
              xCount = symbolCount(a.diagonal(x), "X")
              yCount = symbolCount(a.diagonal(x), "O")
              total += valueAttributor(xCount, yCount)
              print()

       print("diagonal2")
       for x in range(-N + 1, N):
              print(np.flipud(a).diagonal(x))
              xCount = symbolCount(np.flipud(a).diagonal(x), "X")
              yCount = symbolCount(np.flipud(a).diagonal(x), "O")
              total += valueAttributor(xCount, yCount)
              print()

       print(total)


def valueAttributor(countX, countO):
       value = 0
       if countO == 0 and countX == 0:
              return 0
       if countO > countX:
              value = - pow(10,countO)
       else:
              value = pow(10, countX)
       return value




def checkWin(line):
       if (max(consecutiveX(line, 'X')) >= S):
              return 'X'
       if (max(consecutiveX(line, 'O')) >= S):
              return 'O'
       return '.'

print()
def randomBlocks():
       for i in range (0, B):
              x = randint(0, N - 1)
              y = randint(0, N - 1)
              while (a[x][y] != '.'):
                     x = randint(0, N - 1)
                     y = randint(0, N - 1)
              a[x][y] = '#'



print()

def insertBlocks(blocksLocations):
       for i in blocksLocations:
              a[i[0]][i[1]] = '#'

insertBlocks([(0,0),(0,2)])

print(a)



print()
print("verticals")
for x in range (0,N):
       print(a[:,x])
       print(heuristicLong(a[:,x]))
       print()
print()

print()
print("horrizontals")
for x in range (0,N):
       print(a[x])
       print(heuristicLong(a[x]))
print()

print("diagonal1")
for x in range (-N + 1, N):
       print(a.diagonal(x))
       print(heuristicLong(a.diagonal(x)))
print()

print("diagonal2")
for x in range (-N + 1, N):
       print(np.flipud(a).diagonal(x))
       print(heuristicLong(np.flipud(a).diagonal(x)))
print()
#
class toy:
       def __init__(self, n):
              self.n = n

       def test(self):
              print(self.n)

game = toy(4)
game.test()
import numpy as np

game= [['.','.','X','#','X'],
       ['X','.','X','X','O'],
       ['#','X','.','#','.'],
       ['.','#','X','X','O'],
       ['X','O','#','O','O']]
N = 5
S = 4
B = 1
a = np.array(game)
# a = np.arange(25).reshape(N,N)
# a = np.full((N,N), '.')
print(a)


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


def symbolCount(line, symbol):
    counter = 0
    for char in line:
        if (char == symbol):
            counter += 1
    return counter

def valueCounter(line):
    winningLinesX = 0
    winningLinesO = 0
    countX = symbolCount(line, 'X')
    countO = symbolCount(line,'O')
    consecutiveWinX = consecutivePlus(line, 'X')
    consecutiveWinO = consecutivePlus(line, 'O')

    for i in consecutiveWinX:
        if (i >= S):
            winningLinesX+= 1
    for j in consecutiveWinO:
        if (j >= S):
            winningLinesO+= 1

    print(consecutiveWinX)
    print(consecutiveWinO)
    print(winningLinesX)
    print(winningLinesO)
    print(countX)
    print(countO)
    print()
    print((winningLinesX * pow(10, countX)) - (winningLinesO * pow(10, countO)))

    return (winningLinesX * pow(10, countX)) - (winningLinesO * pow(10, countO))


def heuristicLong(game):
    total = 0

    print("verticals")
    for x in range(0, N):
        print(a[:, x])
        total += valueCounter(a[:, x])
    print()

    print("horrizontals")
    for x in range(0, N):
        print(a[x])
        total += valueCounter(a[x])
    print()

    print("diagonal1")
    for x in range(-N + 1, N):
        print(a.diagonal(x))
        total += valueCounter(a.diagonal(x))
    print()

    print("diagonal2")
    for x in range(-N + 1, N):
        print(np.flipud(a).diagonal(x))
        total += valueCounter(np.flipud(a).diagonal(x))
    print()

    return total

print(heuristicLong(game))
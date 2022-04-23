import os
from time import sleep
import re

from Decorators import calculate_time

# All possible items
possible = set('123456789')

# Load puzzle into memory
def load(name):
    puzzle = []
    with open('puzzles/'+name, 'r') as f:
        puzzle = re.sub(r"[^1-9]", ' ', f.read().replace('\n',''))[:81]
        puzzle = [list(puzzle[i:i + 9]) for i in range(0, len(puzzle), 9)]
    return puzzle

def printPuzzle(puzzle, steps = 0, snapshots = 0, snapshotsTaken = 0):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(' ','-'*17)
    for x in range(9):
        print('', end=' | ')
        for y in range(9):
            print(puzzle[x][y], end='')
            if y%3 == 2:
                print(' | ', end='')
        print('')
        if x%3 == 2:
            print(' ', '-'*17)
    print('Steps:', steps)
    print('Snapshots:', snapshotsTaken, ' (', snapshots, ')')

def getPossibleOptions(puzzle, x, y):    
    # Get all items in rows and columns excluding current cell
    row = puzzle[x]
    column = [r[y] for r in puzzle]
    
    # Get all items in grid excluding current cell
    grid = []
    xGrid = x//3
    yGrid = y//3
    for i in range(xGrid*3, (xGrid+1)*3):
        for j in range(yGrid*3, (yGrid+1)*3):
            if i != x or j != y:
                grid.append(puzzle[i][j])

    # Get all invalid items
    options = set().union(row, column, grid)

    # Get all possible items
    return possible.difference(options)

def isComplete(puzzle):
    return not any(' ' in row for row in puzzle)

@calculate_time
def solve(puzzle):
    puzzleSnapshots = []
    
    # Metrics ---------
    steps = 0
    snapshotsTaken = 0
    # -----------------

    while True:
        while True:
            # Display -----------
            # printPuzzle(puzzle, steps, len(puzzleSnapshots), snapshotsTaken)
            # sleep(.25)
            # -------------------

            steps += 1
            
            # Look for cell with lowest entropy
            # aka: fewest possible options but > 1
            minX = -1
            minY = -1
            minOptions = []
            minOptLen = 1
            while minOptLen == 1:
                minX = -1
                minY = -1
                minOptions = ['']*10
                minOptLen = 10

                for x in range(9):
                    for y in range(9):
                        if puzzle[x][y] == ' ':
                            options = getPossibleOptions(puzzle, x, y)
                            if len(options) < minOptLen:
                                minX = x
                                minY = y
                                minOptions = options
                                minOptLen = len(minOptions)

                                # if only 1 option then break x,y loop early and set the value
                                if minOptLen == 1 or minOptLen == 0:
                                    break
                    else:
                        continue
                    break
                # Set cell w/ 1 option and continue loop
                if minOptLen == 1:
                    puzzle[minX][minY] = minOptions.pop()

            # We couldn't find any unfilled cells
            # break to check if solved
            if minX == -1:
                break

            # Take a snapshot if more than 1 option
            if minOptLen > 1:
                snapshotsTaken += 1
                minOptions = list(minOptions)
                puzzleSnapshots.append([[row[:] for row in puzzle], (minX, minY), minOptions[1:]])
                puzzle[minX][minY] = minOptions[0]
            else:
                # No options left, check if solved
                break

        if isComplete(puzzle):
            printPuzzle(puzzle, steps, len(puzzleSnapshots), snapshotsTaken)
            return puzzle
        else:
            # roll back to last snapshot and pick the next option
            (puzzle, (x, y), options) = puzzleSnapshots[-1]
            puzzle[x][y] = options[0]
            if len(options) == 1:
                puzzleSnapshots.pop()
            else:
                puzzleSnapshots[-1][2] = options[1:]

puzzleName = 'puzzle9.txt'
puzzle = load(puzzleName)
solve(puzzle)

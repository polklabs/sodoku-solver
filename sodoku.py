import os
from time import sleep

from pandas import array

from Decorators import calculate_time

# Load puzzle into memory
def load(name):
    puzzle = []
    with open('puzzles/'+name, 'r') as f:
        puzzle = f.read().replace('.', ' ').split('\n')
        puzzle = [list(p) for p in puzzle]
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
    # All possible items
    possible = set('123456789')
    
    # Get all items in rows and columns excluding current cell
    row = [puzzle[x][i] for i in range(len(puzzle[x])) if i != y]
    column = [puzzle[i][y] for i in range(len(puzzle)) if i != x]
    
    # Get all items in grid excluding current cell
    grid = []
    xGrid = x//3
    yGrid = y//3
    for i in range(xGrid*3, (xGrid+1)*3):
        for j in range(yGrid*3, (yGrid+1)*3):
            if i != x or j != y:
                grid.append(puzzle[i][j])

    # Get all possible items that aren't already included
    row = possible.difference(set(row))
    column = possible.difference(set(column))
    grid = possible.difference(set(grid))

    # Get all common possible items
    options = row.intersection(column).intersection(grid)
    return options

def isValidState(puzzle):
    for x in range(9):
        for y in range(9):
            options = getPossibleOptions(puzzle, x, y)
            if len(options) <= 0 or (puzzle[x][y] != ' ' and puzzle[x][y] not in options):
                return False
    return True

def isComplete(puzzle):
    for x in range(9):
        for y in range(9):
            if puzzle[x][y] == ' ':
                return False
    return True

@calculate_time
def solve(puzzle):
    puzzleSnapshots = []
    # Which option to take if we have multiple
    optionNum = 0
    
    # Metrics ---------
    steps = 0
    snapshotsTaken = 0
    # -----------------

    while True:
        while isValidState(puzzle):
            # Display -----------
            # printPuzzle(puzzle, steps, len(puzzleSnapshots), snapshotsTaken)
            # sleep(.25)
            # -------------------

            steps += 1
            
            # Look for cell with lowest entropy
            # aka: fewest possible options but > 1
            minX = -1
            minY = -1
            minOptions = ['']
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
                                if minOptLen == 1:
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
                # If we've exhausted all options then get previous snapshot
                if minOptLen <= optionNum:
                    break
                snapshotsTaken += 1
                puzzleSnapshots.append(([row[:] for row in puzzle], optionNum))
                
                # Make sure options are always in the same order
                minOptions = list(minOptions)
                minOptions.sort()
                puzzle[minX][minY] = minOptions[optionNum]
                
                optionNum = 0 # set back to 0 for next choice we come across
            else:
                # No options left, check if solved
                break

        if isComplete(puzzle) and isValidState(puzzle):
            printPuzzle(puzzle, steps, len(puzzleSnapshots), snapshotsTaken)
            return puzzle
        else:
            # roll back to last snapshot and increment the option index to choose
            (puzzle, optionNum) = puzzleSnapshots.pop()
            optionNum += 1

puzzleName = 'puzzle5.txt'
puzzle = load(puzzleName)
solve(puzzle)
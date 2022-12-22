import numpy as np


def isVisible(forestMap: np.ndarray, treeLocation: tuple[int, int]) -> bool:
    """
    finds out if the tree at (treeRow, treeCol) in the forestMap is visible from outside the forest
    """
    treeRow, treeCol = treeLocation
    treeHeight = forestMap[treeRow, treeCol]
    lastRow = len(forestMap) - 1
    lastCol = len(forestMap[0]) - 1

    # trees on the perimeter of the forest are visible
    onPerimeter = (treeCol == 0) or (treeCol == lastCol) or (treeRow == 0) or (treeRow == lastRow)
    # is the tree visible from the north or the south?
    north = np.all(forestMap[:treeRow, treeCol] < treeHeight)
    south = np.all(forestMap[treeRow + 1:, treeCol] < treeHeight)
    # is the tree visible from the east or the west?
    west = np.all(forestMap[treeRow, :treeCol] < treeHeight)
    east = np.all(forestMap[treeRow, treeCol + 1:] < treeHeight)

    return onPerimeter or north or east or south or west


def viewingDist(treeLine: np.ndarray) -> int:
    """
    Calculates how many trees in treeLine can be seen from the first tree in the
    """
    if len(treeLine) <= 1:
        return 0

    dist = 0
    treeHeight = treeLine[0]

    for tree in treeLine[1:]:
        dist += 1
        if tree >= treeHeight:
            break
    return dist


def scenicScore(forestMap: np.ndarray, treeLocation: tuple[int, int]) -> int:
    """
    A tree's scenic score is found by multiplying together its viewing distance in each of the four directions.
    """
    treeRow, treeCol = treeLocation
    treeHeight = forestMap[treeRow, treeCol]

    toNorth = viewingDist(np.flip(forestMap[:treeRow + 1, treeCol]))
    toSouth = viewingDist(forestMap[treeRow:, treeCol])
    toEast = viewingDist(forestMap[treeRow, treeCol:])
    toWest = viewingDist(np.flip(forestMap[treeRow, :treeCol+1]))

    return toNorth * toEast * toSouth * toWest


file = open('test')
text = file.read().strip().split('\n')
file.close()

# read the input file character by character and convert it into a 2d array of ints
forestMap = np.array(list(map(list, text)), dtype=int)
rows, cols = forestMap.shape

# record which trees are visible from outside the forest and the scenic score of each tree
visibleMap = np.zeros((rows, cols), dtype=bool)
scenicMap = np.zeros((rows, cols), dtype=int)

for row in range(rows):
    for col in range(cols):
        visibleMap[row, col] = isVisible(forestMap, (row, col))
        scenicMap[row, col] = scenicScore(forestMap, (row, col))

print(f"The number of visible trees is: {visibleMap.sum()}")
print(f"The highest scenic score possible is: {scenicMap.max()}")

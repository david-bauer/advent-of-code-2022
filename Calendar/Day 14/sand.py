import numpy as np


class Rect:
    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.width = xmax - xmin + 1
        self.height = ymax - ymin + 1


def parse_path(path_text):
    """Extract all the points from the string. Returns a list of points"""
    return np.array([np.array(point.split(','), dtype=int) for point in path_text.split(' -> ')])


def get_boundary(points):
    """
    Returns a rectangle representing the smallest area we will have to model
    The sand starts falling from (500, 0), and the floor is located 2 steps below the point with the largest y coord.
    The sand can at most move one unit horizontally for every unit it falls vertically, so the boundary will be a square
    horizontally centered around (500, 0) with a height determined by the point with the largest y coordinate
    """
    y_values = points[:,1]
    height = np.max(y_values) + 2
    return Rect(500 - height, 500 + height, 0, height)


def move_sand(pos, area_is_filled):
    """returns the next possible position of the sand"""
    down = (pos[0], pos[1] + 1)
    left = (pos[0] - 1, pos[1] + 1)
    right = (pos[0] + 1, pos[1] + 1)

    # the sand has reached the floor
    if down[1] >= area_is_filled.shape[1] - 1:
        return pos

    try:
        if not area_is_filled[down]:
            # move the sand down if possible
            return down
        elif not area_is_filled[left]:
            # then try down-left
            return left
        elif not area_is_filled[right]:
            # finally try down-right
            return right
        else:
            return pos
    except IndexError:
        # the sand has reached the bottom
        return pos


with open('input') as file:
    text = file.read().strip().split('\n')

# read the paths from the file
paths = []
points = []
for path_text in text:
    paths.append(parse_path(path_text))
    points.extend(paths[-1])
points = np.array(points)

# determine the boundary box of the minimum area we have to model
boundary = get_boundary(points)
# create the model and fill the spaces that are occupied by paths
cave = np.zeros((boundary.width, boundary.height), dtype=bool)
for path in paths:
    # each path is defined by a series of lines
    for i in range(1, len(path)):
        # lines can only be horizontal or vertical
        start = path[i - 1]
        end = path[i]
        # fill all the points contained in this line
        if start[1] == end[1]:  # line is horizontal
            for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
                cave[x - boundary.xmin, start[1] - boundary.ymin] = True
        else:  # line is vertical
            for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                cave[start[0] - boundary.xmin, y - boundary.ymin] = True

# start simulating the sand until the drop point becomes filled
sand_count = 0
drop_pos = (500 - boundary.xmin, 0)
while not cave[drop_pos]:
    sand_count += 1
    # drop a single grain of sand
    sand_pos = None
    next_pos = drop_pos
    # simulate the sand falling until it comes to a stop
    while next_pos != sand_pos:
        sand_pos = next_pos
        next_pos = move_sand(sand_pos, cave)
    # update the model--consider the position the sand settled in as filled
    cave[sand_pos] = True

print(f"{sand_count} units of sand came to rest before the cave was filled")  #24377

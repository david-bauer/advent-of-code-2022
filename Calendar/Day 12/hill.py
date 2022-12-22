import numpy as np
from dataclasses import dataclass, field
from typing import Tuple, List, Callable
from queue import PriorityQueue


@dataclass(order=True)
class Node:
    dist: float
    pos: Tuple[int, int] = field(compare=False)


def convert_to_elevation(character: str) -> int:
    if character == 'S':
        return 0
    elif character == 'E':
        return ord('z') - ord('a')
    else:
        return ord(character) - ord('a')


def get_unvisited_neighbors(pos: Tuple[int, int], visited: List[Tuple[int, int]], test: Callable, elevation_map) -> \
        List[Tuple[int, int]]:
    """
    Return a list of unvisited positions adjacent to the one provided that pass a test.
    The callback function 'test' is passed the position, the position of a neighbor, and the elevation map

    :param pos: a tuple containing the row and the column of the inspected position
    :type pos: tuple
    :param visited: a list containing all the positions that have been visited so far
    :type visited: list[tuple[int, int]]
    :param test: a callback function that determines if a neighbor can be reached
    :type test: callable[[tuple[int, int], tuple[int, int], any], bool]
    :param elevation_map: A numpy array representing the elevation at a certain position in the hill being traversed
    :type elevation_map: np.array
    :return A list containing reachable positions adjacent to the one provided
    """

    row, col = pos
    valid_moves = []

    # check the northern neighbor
    neighbor = (row - 1, col)
    if 0 < row and test(pos, neighbor, elevation_map) and neighbor not in visited:
        valid_moves.append(neighbor)

    # check the western neighbor
    neighbor = (row, col - 1)
    if 0 < col and test(pos, neighbor, elevation_map) and neighbor not in visited:
        valid_moves.append(neighbor)

    # check the southern neighbor
    neighbor = (row + 1, col)
    if neighbor[0] < elevation_map.shape[0] and test(pos, neighbor, elevation_map) and neighbor not in visited:
        valid_moves.append(neighbor)

    # check the eastern neighbor
    neighbor = (row, col + 1)
    if neighbor[1] < elevation_map.shape[1] and test(pos, neighbor, elevation_map) and neighbor not in visited:
        valid_moves.append(neighbor)

    return valid_moves


def find_shortest_path(start_pos: Tuple[int, int], end_condition: Callable,
                       move_condition: Callable, elevation_map) -> float:
    """
    Use Dijkstra's algorithm to find the shortest path from the starting position to the ending position in the hill
    :param start_pos: The row and column of the starting position in the hill
    :type start_pos: tuple[int, int]
    :param end_condition: A callback function that indicates if the ending position has been reached
    :param move_condition: A callback function that determines if a position can be reached from a neighboring position
    :param elevation_map: A numpy array representing the elevations of a hill
    :type elevation_map: np.array[int]
    :return: A list of paths (a list of positions) from the starting position to the ending position in the hill
    :rtype: list[int]
    """

    # Find the shortest path from the starting position to each position in the hill
    tentative_distances = np.full(elevation_map.shape, np.inf)
    tentative_distances[start_pos] = 0  # the distance from the starting position to itself is zero
    current_node = Node(0, start_pos)
    # Visit the positions closest to the starting position first. Use a priority queue to manage the order in which
    # positions are visited
    unvisited_nodes = PriorityQueue()
    unvisited_nodes.put(current_node)
    visited_positions = []

    # Continually visit the closest unvisited position until the end is reached or there are no more unvisited positions
    while not end_condition(current_node.pos) and not unvisited_nodes.empty():
        current_node = unvisited_nodes.get()
        # Skip positions in the queue that have already been visited
        if current_node.pos in visited_positions:
            continue
        visited_positions.append(current_node.pos)

        # Update the tentative calculation of the min distance from the start to the neighbors of the current position
        for neighbor_pos in get_unvisited_neighbors(current_node.pos, visited_positions, move_condition, elevation_map):
            tentative_distances[neighbor_pos] = min(tentative_distances[neighbor_pos], current_node.dist + 1)
            unvisited_nodes.put(Node(tentative_distances[neighbor_pos], neighbor_pos))
            """
            Updating the priority of a position in the priority queue is hard because we don't know exactly where the
            position is stored. We will rely on the fact that the tentative minimum path to a position can only
            decrease. This means that nodes can only move forward in the priority queue. When we find a shorter path
            to any position, instead of updating the priority of that position, the position will be re-added to the 
            queue but with a higher priority. This will create duplicates in the priority queue that need to be skipped.
            """

    # There will be no unvisited nodes when the end condition is unachievable
    if unvisited_nodes.empty():
        return np.inf
    else:
        return tentative_distances[current_node.pos]


with open('input') as file:
    text = file.read().strip().split('\n')

# read the input file character by character and convert it to a 2d array containing the elevation at points on the hill
rows = len(text)
cols = len(text[0])
elevation_map = np.zeros((rows, cols), dtype=int)
start = None
end = None
for rowNum, row in enumerate(text):
    for colNum, value in enumerate(row):
        here = (rowNum, colNum)
        if value == 'S':
            start = here
        if value == 'E':
            end = here
        elevation_map[here] = convert_to_elevation(value)


# Part 1: find the shortest path from start to end

def climb_one(pos, neighbor, hill):
    # you can climb one elevation per step
    return hill[pos] + 1 >= hill[neighbor]


fewest_steps = find_shortest_path(start, lambda pos: pos == end, climb_one, elevation_map)
print(f"The shortest possible path from {start} to {end} takes {int(fewest_steps)} steps.")


# Part 2: find the shortest path from any square of elevation 'a' to the end

# Work backwards from the end position to any square of elevation a
def fall_one(pos, neighbor, hill):
    # the opposite of climbing one elevation per step (we are working backwards so our travel condition has reversed)
    return hill[pos] - 1 <= hill[neighbor]


fewest_steps_from_a = find_shortest_path(end, lambda pos: elevation_map[pos] == 0, fall_one, elevation_map)
print(f"The shortest possible path from any square of elevation 'a' to {end} takes {int(fewest_steps_from_a)} steps.")

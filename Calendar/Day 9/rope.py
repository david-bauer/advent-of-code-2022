def readVector(instruction: str) -> complex:
    """
    Converts a string containing a direction and a length into a vector (complex number)
    """
    dir = instruction[0]
    dist = int(instruction[2:])

    if dir == 'R':
        return complex(dist, 0)
    if dir == 'L':
        return complex(-dist, 0)
    if dir == 'U':
        return complex(0, dist)
    if dir == 'D':
        return complex(0, -dist)
    raise ValueError(f'Instruction of type {dir} invalid!')


file = open('input')
instructions = file.read().strip().split('\n')
file.close()

rope = [complex(0)] * 10  # rope of length 10
tailTraversed = {complex(0)}  # sets cannot contain duplicates

# move the head of the rope according to each instruction
for move in instructions:
    headVector = readVector(move)
    unitVector = headVector / abs(headVector)
    # break up the large vector into movements of 1 space
    for movement in range(int(abs(headVector))):
        # move the head
        rope[0] += unitVector
        # pull along the rest of the rope
        for i in range(1, len(rope)):
            # if a knot is too far from the previous knot (more than 1 space apart), move the former closer
            vector = rope[i-1] - rope[i]
            if abs(vector) > 2.2:
                # knots are separated diagonally, so move diagonally toward the prev knot
                rope[i] += complex(round(vector.real / abs(vector.real)), round(vector.imag / abs(vector.imag)))
            elif abs(vector) > 1.8:
                # knots are separated horizontally or vertically, so move directly towards the prev knot
                rope[i] += complex(round(vector.real / abs(vector)), round(vector.imag / abs(vector)))

        tailTraversed.add(rope[-1])  # add the position of the tail to the set

print(f'The tail visited {len(tailTraversed)} positions')

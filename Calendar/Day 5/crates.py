file = open('input')
initStructure, instructions = file.read().strip().split('\n\n')
file.close()

initStructure = initStructure.split('\n')
instructions = instructions.split('\n')

# make an array that represents the stacks of crates
totalCrates = int(initStructure.pop().split('   ')[-1])
cargo = [[] for i in range(totalCrates)]

# save the initial arrangement of the crates to cargo
initStructure.reverse()  # we read the rows from top to bottom. The crates on the bottom must be added to cargo first.
for row in initStructure:
    cols = round(len(row) / 4)  # 3 characters per column each with a gap of 1
    crates = list(map(lambda index: row[4*index + 1:4*index + 2], range(cols)))
    for index, crate in enumerate(crates):
        if crate == ' ':
            continue
        cargo[index].append(crate)

# read the instructions and modify the cargo as necessary
for row in instructions:
    parts = row.split(' ')
    numCratesToBeMoved = int(parts[1])
    src = int(parts[3]) - 1
    dest = int(parts[5]) - 1
    movedCrates = []
    for crate in range(numCratesToBeMoved):
        movedCrates.append(cargo[src].pop())
    movedCrates.reverse()  # comment this line out for part 1
    cargo[dest].extend(movedCrates)

# read the crates on the top of each stack
cratesOnTop = ''
for stack in cargo:
    cratesOnTop += stack[-1]
print(f"The crates at the top of each stack are: {cratesOnTop}")
"""
Part 1: VWLCWGSDQ
Part 2: TCGLQSPW
"""

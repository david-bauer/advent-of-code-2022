def runCRT(cycle, spritePos):
    """
    Produces a pixel on the CRT according to the current cycle and the position of the sprite
    """
    if spritePos - 1 <= cycle % 40 <= spritePos + 1:
        # when the sprite is positioned on the next pixel, produce a lit pixel
        print("#", end="")
    else:
        # otherwise produce a dark pixel
        print(".", end="")
    if cycle % 40 == 39:
        # go to the next line after 40 pixels have been drawn
        print("")


def runCPU(cycle: int, X: int) -> int:
    """
    Simulates one clock cycle. Returns the signal strength on cycles 20 and every 40 after
    """
    runCRT(cycle, X)

    cycle += 1

    # record the signal strengths on cycles 20 and every 40 after
    if cycle % 40 == 20:
        return cycle * X
    else:
        return 0


file = open('input')
program = file.read().strip().split('\n')
file.close()

X = 1
cycle = 0
signalStrengths = 0

print("Image produced from CRT:")  # EZFPRAKL

for line in program:
    command = line.split(' ')
    # run one clock cycle
    signalStrengths += runCPU(cycle, X)
    cycle += 1
    # run an extra clock cycle if the command is addx
    if command[0] == "addx":
        signalStrengths += runCPU(cycle, X)
        cycle += 1
        # addx increments X after the second cycle
        X += int(command[1])

print(f"The sum of the six signal strengths is: {signalStrengths}")
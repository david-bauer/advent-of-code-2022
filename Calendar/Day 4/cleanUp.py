class Range:
    def __init__(self, start:int, end:int):
        self.start = start
        self.end = end

    def surrounds(self, other) -> bool:
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other) -> bool:
        return not (self.end < other.start or other.end < self.start)

    def fromString(text:str):
        values = text.split('-')
        return Range(int(values[0]), int(values[1]))

    def __repr__(self):
        return repr((self.start, self.end))


file = open("input")
pairs = file.read().strip().split('\n')
file.close()

numSurrounded = 0
numOverlapping = 0

for pair in pairs:
    ranges = pair.split(',')
    rangeA = Range.fromString(ranges[0])
    rangeB = Range.fromString(ranges[1])

    if rangeA.surrounds(rangeB) or rangeB.surrounds(rangeA):
        numSurrounded += 1

    if rangeA.overlaps(rangeB):
        numOverlapping += 1

print(f"Number of pairs in which one range fully contains the other: {numSurrounded}")
print(f"Number of pairs in which one range overlaps the other: {numOverlapping}")

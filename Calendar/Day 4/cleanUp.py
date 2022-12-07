class Range:
    def __init__(self, start:int, end:int):
        self.start = start
        self.end = end

    def surrounds(self, other) -> bool:
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other) -> bool:
        for value in self:
            if value in other:
                return True
        return False

    def fromString(text:str):
        values = text.split('-')
        return Range(int(values[0]), int(values[1]))

    def __contains__(self, item:int) -> bool:
        return self.start <= item <= self.end

    def __len__(self) -> int:
        return self.end - self.start + 1

    def __lt__(self, other) -> bool:
        if self.__len__() == other.__len__():
            return self.start < other.end
        return self.__len__() < other.__len__()

    def __eq__(self, other) -> bool:
        return self.__len__() == other.__len__() and self.start == other.start and self.end == other.end

    def __iter__(self):
        self.iterator = self.start
        return self

    def __next__(self):
        if self.iterator <= self.end:
            result = self.iterator
            self.iterator += 1
            return result
        else:
            raise StopIteration

    def __repr__(self):
        return repr((self.start, self.end, self.__len__()))

    def __str__(self):
        return f"{self.start}-{self.end}"


file = open("input")
numSurrounded = 0
numOverlapping = 0
for line in file:
    if line == '':
        continue

    ranges = line.split(',')
    rangeA = Range.fromString(ranges[0])
    rangeB = Range.fromString(ranges[1])

    if rangeA.surrounds(rangeB) or rangeB.surrounds(rangeA):
        numSurrounded += 1

    if rangeA.overlaps(rangeB):
        numOverlapping += 1

print(f"Number of pairs in which one range fully contains the other: {numSurrounded}")
print(f"Number of pairs in which one range overlaps the other: {numOverlapping}")

file.close()

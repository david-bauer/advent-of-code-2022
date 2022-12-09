class File:
    def __init__(self, name: str, parent, size: int):
        self.name = name
        self.parent = parent
        self.size = size

        if parent:
            self.parent.children.append(self)

    def getSize(self) -> int:
        return self.size

    def __add__(self, other) -> int:
        return self.getSize() + other

    def __radd__(self, other) -> int:
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __lt__(self, other):
        return self.getSize() < other.getSize()

    def __repr__(self) -> str:
        return repr((self.name, self.getSize()))


class Directory(File):
    def __init__(self, name: str, parent):
        super().__init__(name, parent, 0)
        self.children = []

    def getSize(self) -> int:
        total = 0
        if len(self.children) == 0:
            return 0
        for child in self.children:
            total += child.getSize()
        return total

    def getChild(self, childName: str) -> File:
        for child in self.children:
            if child.name == childName:
                return child
        return None


currentDir: Directory = Directory('/', None)
dirList: [Directory] = [currentDir]

file = open('input')
# process the terminal output line by line
for terminalLine in file:
    if terminalLine == '':
        continue

    parse = terminalLine[:-1].split(' ')
    # process commands
    if parse[0] == '$':
        cName = parse[1]
        if cName == 'cd': # change current directory command
            dirName = parse[2]
            if dirName == '/': # go to root
                currentDir = dirList[0]

            elif dirName == '..': # go up a level
                currentDir = currentDir.parent

            else:  # move to the directory specified if it exists
                nextDir = currentDir.getChild(dirName)
                if nextDir:
                    currentDir = nextDir
                else:  # if the directory doesn't exist, make it
                    currentDir = Directory(parse[2], currentDir)
                    dirList.append(currentDir)

    elif parse[0] == 'dir': # terminal printed a directory
        dirName = parse[1]
        # if the directory doesn't already exist, make it
        if not currentDir.getChild(dirName):
            newDir = Directory(dirName, currentDir)
            dirList.append(newDir)

    else: # terminal printed a file
        size = int(parse[0])
        name = parse[1]
        # if the file doesn't already exist, make it
        if not currentDir.getChild(name):
            newFile = File(name, currentDir, size)

file.close()

smallFolders = list(filter(lambda folder: folder.getSize() <= 100000, dirList))
print(f"The sum of all the directories with a size of at most 100000 is: {sum(smallFolders)}")

freeSpace = 70000000 - dirList[0].getSize()
neededSpace = 30000000 - freeSpace
deleteTargets = list(filter(lambda folder: folder.getSize() >= neededSpace, dirList))
deleteTargets.sort()
print(f"The size of the smallest directory that could be deleted to free up enough space to update is: {deleteTargets[0].getSize()}")

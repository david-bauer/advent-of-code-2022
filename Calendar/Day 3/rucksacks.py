def findCommonChars(*strings: str) -> list[str]:
    """
    returns a list of the characters that are included in every argument
    """
    commonChars = []
    # compare each character in the first string with all the characters in the other strings
    for char in strings[0]:
        allStringsIncludeChar = True
        for string in strings[1:]:
            if not char in string:
                allStringsIncludeChar = False
                break;
        if allStringsIncludeChar and not char in commonChars:
            commonChars.append(char)
    return commonChars


def priority(char: str) -> int:
    """
    calculates the priority value of the character
    """
    if ord(char) < ord('a'):
        # uppercase
        return ord(char) - ord('A') + 27
    else:
        # lowercase
        return ord(char) - ord('a') + 1


file = open('input')
rucksacks = file.read().strip().split('\n')
file.close()

prioritySum = 0

for rucksack in rucksacks:
    # each rucksack has two equally filled compartments
    barrier = int(len(rucksack) / 2)
    part1 = rucksack[:barrier]
    part2 = rucksack[barrier:]

    commonChars = findCommonChars(part1, part2)
    for common in commonChars:
        prioritySum += priority(common)

print(f"The sum of the priorities is: {prioritySum}")

badges = []
numGroups = int( len(rucksacks) / 3 )
for index in range(numGroups):
    badges.extend(findCommonChars(rucksacks[3 * index], rucksacks[3 * index + 1], rucksacks[3 * index + 2]))

badgePrioritySum = 0
for badge in badges:
    badgePrioritySum += priority(badge)
print(f"The sum of the priorities of the badges is: {badgePrioritySum}")

file.close()
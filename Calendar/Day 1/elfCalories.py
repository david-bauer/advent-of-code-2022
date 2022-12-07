file = open("input")
# file = open("test")
caloryCount = []
elves = file.read().split('\n\n')
for elf in elves:
    backpack = elf.split('\n')
    sum = 0
    for item in backpack:
        if item == '':
            break
        sum += int(item)
    caloryCount.append(sum)
caloryCount.sort(reverse=True)
print(f"Part 1: The elf with the most calories has {caloryCount[0]} calories")
top3Sum = 0
for cal in caloryCount[0:3]:
    top3Sum += cal
print(f"Part 1: The top 3 elves with the most calories have {top3Sum} calories")
file.close()
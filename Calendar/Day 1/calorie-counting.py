file = open("input")
elves = file.read().strip().split('\n\n')
file.close()

# order the elves by calorie count
caloryCount = []

for elf in elves:
    # sum up the calories stored in each elf's backpack
    backpack = elf.split('\n')
    calories = [int(item) for item in backpack]
    caloryCount.append(sum(calories))
caloryCount.sort(reverse=True)

# find the calories carried by the elf with the most calories
print(f"Part 1: The elf with the most calories has {caloryCount[0]} calories")

# find the total calories stored by the 3 elves with the most calories
top3Sum = sum(caloryCount[0:3])
print(f"Part 1: The top 3 elves with the most calories have {top3Sum} calories")

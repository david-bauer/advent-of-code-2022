class Item:
    def __init__(self, base):
        # The monkies rely on the modulus of the worry level to determine who to throw the item to next.
        # Instead of recording the full worry level of each item (which can become backbreakingly large after just
        # a few hundred rounds), record only the data that is neccessary: the modulus of the worry level.
        # Each monkey has a different divisor, so we must record the modulus of the worry level for every divisor.
        divisors = [2, 3, 5, 7, 11, 13, 17, 19, 23]
        self.divisor_to_remainder = { divisor: base % divisor for divisor in divisors }

    def add(self, num):
        # the modulus operator is distributive for addition:
        # (A + B) % divisor = (A % divisor + B % divisor) % divisor
        self.divisor_to_remainder = {
            divisor: (remainder + num % divisor) % divisor for divisor, remainder in self.divisor_to_remainder.items()
        }
        return self.divisor_to_remainder

    def multiply(self, num):
        # the modulus operator is also distributive for products:
        # (A * B) % divisor = (A % divisor * B % divisor) % divisor
        self.divisor_to_remainder = {
            divisor: (remainder * (num % divisor)) % divisor for divisor, remainder in self.divisor_to_remainder.items()
        }
        return self.divisor_to_remainder

    def square(self):
        # special case of multiplicatoon
        self.divisor_to_remainder = {
            divisor: (remainder**2) % divisor for divisor, remainder in self.divisor_to_remainder.items()
        }
        return self.divisor_to_remainder

    def __repr__(self):
        return repr(self.divisor_to_remainder)


def monkey_operation_factory(operator: str, value: str) -> callable:
    """
    A function factory that creates a function that a Monkey object will use to increase the worry level of an item.
    Each monkey affects an item's worry level differently.
    :param operator: Either '+' or '*', representing addition or multiplication
    :type operator: str
    :param value: Value to add to or multiply with this item. If value is 'old', the item will be squared instead.
    :type value: str
    :return: a function that increases the worry level of an item according to a Monkey's unique personality
    :rtype: callable
    """
    try:
        amplitude = int(value)
        if operator == '+':
            def operation(item: Item) -> Item:
                return item.add(amplitude)

        elif operator == '*':
            def operation(item: Item) -> Item:
                return item.multiply(amplitude)

    except:
        # value is the string "old" and cannot be converted to int
        def operation(item: Item) -> Item:
            return item.square()

    return operation


class Monkey:
    def __init__(self, index: int, items: list, operator: str, amplitude: str, divisor: int, if_true: int, if_false: int):
        self.index = index
        self.items = list(map(Item, items))
        self.operation = monkey_operation_factory(operator, amplitude)
        self.amplitude = amplitude
        self.divisor = divisor
        self.if_true = if_true
        self.if_false = if_false
        self.items_inspected = 0


    def test(self, divisor_to_remainder: int) -> bool:
        return divisor_to_remainder[self.divisor] == 0

    def __repr__(self):
        return f"Monkey {self.index}: {self.items} items, {self.items_inspected} items inspected"


file = open('input')
monkeyFile = file.read().strip().split('\n\n');
file.close()

# create the Monkey objects from the input file
def parseMonkey(monkeyString):
    notes = monkeyString.split('\n');
    index = int(notes[0][len("Monkey ")])
    items = list(map(int, notes[1][len("  Starting items: "):].split(', ')))
    operator = notes[2][len("  Operation: new = old ")]
    value = notes[2][len("  Operation: new = old X "):]
    divisor = int(notes[3][len("  Test: divisible by "):])

    if_true = int(notes[4][len("    If true: throw to monkey "):])
    if_false = int(notes[5][len("    If false: throw to monkey "):])
    return (Monkey(index, items, operator, value, divisor, if_true, if_false))

monkeys = list(map(parseMonkey, monkeyFile))


# simulate each round
rounds = 10000
for round in range(rounds):
    for monkey in monkeys:
        # count the number of items the monkey will inspect & throw
        monkey.items_inspected += len(monkey.items)
        # throw each item to another monkey
        while (len(monkey.items) > 0):
            item = monkey.items.pop()
            monkeys[monkey.if_true if monkey.test(monkey.operation(item)) else monkey.if_false].items.append(item)

    # print progress to console every now and then
    if round % (rounds / 10) == rounds / 10 - 1:
        print(f"== After round {round + 1} / {rounds} ==")
        for monkey in monkeys:
            print(f"Monkey {monkey.index} inspected items {monkey.items_inspected} times.")
        print("\n")

# calculate the level of "monkey business" that occured:
# monkey business = the product of the number of items inspected by the two most active monkies
monkeys.sort(key = lambda monkey: monkey.items_inspected, reverse=True)
monkey_business = monkeys[0].items_inspected * monkeys[1].items_inspected

print(f"The level of monkey business is: {monkey_business}")  # 14081365540
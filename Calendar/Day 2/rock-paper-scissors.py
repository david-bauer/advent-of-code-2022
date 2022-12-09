def battle(you: int, opp: int) -> int:
    """
    returns an integer according to the outcome of a game of rock paper scissors:
    1st argument wins: 1
    1st argument ties: 0
    1st argument loses: -1
    """
    if (you == opp): # tie
        return 0

    if you == 1:  # rock
        if opp == 2:  # paper
            return -1
        if opp == 3:  # scissors
            return 1

    if you == 2:  # paper
        if opp == 1:  # rock
            return 1
        if opp == 3:  # scissors
            return -1

    if you == 3:  # scissors
        if opp == 1:  # rock
            return -1
        if opp == 2:  # paper
            return 1
    raise Exception(f"Incorrect values passed to battle(you, opp): {you}, {opp}")


def getMove(oppChar: str, outcome: str) ->str:
    """
    returns a character representing what should be played to get an outcome given the opponents move
    """
    opp = ord(oppChar) - ord('A') # 0 if rock, 1 if paper, 2 if scissors
    yourMove = ''
    if outcome == 'X': # lose
        yourMove = (opp + 2) % 3
    if outcome == 'Y': # tie
        yourMove = opp
    if outcome == 'Z': # win
        yourMove = (opp + 1) % 3

    return chr(yourMove + ord('X'))


def score(youChar, oppChar):
    """
    returns the points awarded for a match of rock paper scissors.
    points are calculated by the formula:   (points for outcome + points for pick)
        points for outcome: 0 for loss, 3 for tie, 6 for win
        points for pick: 0 for rock, 1 for paper, 2 for scissors
    """
    # calculate point value of pick
    you = ord(youChar) - ord('X') + 1
    opp = ord(oppChar) - ord('A') + 1

    return 3 + 3 * battle(you, opp) + you


file = open('input')
tournament = file.read().strip.split('\n')
file.close()

badSum = 0
goodSum = 0

for round in tournament:
    if round == '':
        break
    # 1st char represents opponent's move, 3rd char represents your move
    badSum += score(round[2], round[0])
    goodSum += score(getMove(round[0], round[2]), round[0])

print(f"Sum of your points if you followed the assumed strategy guide: {badSum}")
print(f"Sum of your points if you followed the correct strategy guide: {goodSum}")

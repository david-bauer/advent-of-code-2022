def eachUnique(test: str) -> bool:
    """ Test if each character in the given string is unique """
    occurred = ''
    for item in test:
        if item in occurred:
            return False
        occurred += item
    return True


def slide(target: str, newItem: str) -> str:
    """ Removes the first character from the string and adds a new one """
    return target[1:] + newItem


file = open('input')
signal = file.read()
file.close()

packetMarker = signal[0:4]
messageMarker = signal[0:14]
firstMarker = None
firstMessage = None
for index, char in enumerate(signal):
    # add the char to the markers
    packetMarker = slide(packetMarker, char)
    messageMarker = slide(messageMarker, char)

    # test the markers
    if (not firstMarker) and eachUnique(packetMarker):
        firstMarker = index + 1

    if (not firstMessage) and eachUnique(messageMarker):
        firstMessage = index + 1

if firstMarker:
    print(f"The first marker is after character {firstMarker}")
else:
    print(f"There is no marker")

if firstMessage:
    print(f"The first message is after character {firstMessage}")
else:
    print(f"There is no message")

import re
from functools import cmp_to_key, reduce

SEPARATORS = re.compile(r'[,\]]')


def parse_packet(untrimmed_packet_text: str):
    """generate a 'packet' from a string representation of a comma separated list containing integers and sublists"""

    packet_text = untrimmed_packet_text[1:]
    packet = []
    index = 0
    while 0 <= index < len(packet_text):
        if packet_text[index] == '[':
            # add a sublist to the packet and skip to the next item
            packet.append(parse_packet(packet_text[index:]))
            index += 1 + 2 * len(packet[-1])

        elif packet_text[index] == ']':
            # a sublist has completed, return its contents
            return packet

        elif packet_text[index].isnumeric():
            # add a number to the packet and move to the next item
            separator_match = SEPARATORS.search(packet_text[index + 1:])
            segment_end = index + separator_match.span()[0]
            packet.append(int(packet_text[index:segment_end + 1]))
            index = segment_end

        index += 1

    return packet


def compare_packets(first_packet, second_packet) -> int:
    """
    Compare the items, sublists, and lengths of each packet to determine which packet should come first.
    Returns:
        a negative value when first_packet < second_packet,
        0 when first_packet == second_packet,
        a positive value when first_packet > second_packet
    """

    for first_item, second_item in zip(first_packet, second_packet):
        # compare the next items if these two are identical
        if first_item == second_item:
            continue

        # If both items are integers, the lower integer should come first
        if type(first_item) == int and type(second_item) == int:
            return first_item - second_item

        # If both items are lists, recursively compare each sub item in the lists
        if type(first_item) == list and type(second_item) == list:
            return compare_packets(first_item, second_item)

        # If one of the items is a list and the other an int, convert the former to a list and recursively compare each sub item
        if type(first_item) != type(second_item):
            if type(first_item) == int and not [first_item] == second_item:
                return compare_packets([first_item], second_item)
            elif type(second_item) == int and not first_item == [second_item]:
                return compare_packets(first_item, [second_item])

    # if none of the items in the packets caused a comparison, the shorter packet should come first
    return len(first_packet) - len(second_packet)


with open('input') as file:
    text = file.read().strip().split('\n\n')

ordered_pairs = []  # record the indices of the packet pairs that are already in the correct order
packets = []  # assemble a list of every packet so that we can sort it and calculate the decoder key

for index, packet_pair_text in enumerate(text):
    # Parse each pair of packets and compare them. If a pair is already in the correct order, record its index
    packet_pair = [parse_packet(packet_text) for packet_text in packet_pair_text.split('\n')]
    if compare_packets(*packet_pair) < 0:
        ordered_pairs.append(index + 1)
    packets.extend(packet_pair)

print(f"The sum of the indices of the pairs already in the correct order is: {sum(ordered_pairs)}")  # 5252

# Calculate the decoder key
divider_packets = [[[2]], [[6]]]
# Insert the divider packets
packets.extend(divider_packets)
# Sort the packets according to the comparison algorithm
packets.sort(key=cmp_to_key(compare_packets))
# Find the indices of the divider packets in the new sorted list
divider_indices = [packets.index(divider_packet) + 1 for divider_packet in divider_packets]
# Multiply the indices of the divider packets to calculate the decoder key
decoder_key = reduce(lambda x, y: x * y, divider_indices)

print(f"The decoder key for the distress signal is {decoder_key}")  # 20592

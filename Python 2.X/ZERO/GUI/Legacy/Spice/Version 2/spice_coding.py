import random, spice_key

def encode(major_key, minor_key, old_string):
    map_1 = spice_key.get_right_side(major_key)
    map_2 = minor_for_encode(minor_key)
    new_string = str()
    for character in old_string:
        number = map_1[ord(character)]
        new_string += chr(map_2[(number >> 6) & 3][random.randint(0, 63)]) \
        + chr(map_2[(number >> 4) & 3][random.randint(0, 63)]) \
        + chr(map_2[(number >> 2) & 3][random.randint(0, 63)]) \
        + chr(map_2[(number >> 0) & 3][random.randint(0, 63)])
    return new_string

def minor_for_encode(minor_key):
    map_2 = [[], [], [], []]
    for character, digit in minor_key:
        map_2[digit].append(character)
    return map_2

def decode(major_key, minor_key, old_string):
    map_1 = spice_key.get_right_side(minor_key)
    map_2 = spice_key.get_left_side(major_key)
    new_string = str()
    for index in range(len(old_string) / 4):
        new_string += chr(map_2[(map_1[ord(old_string[index * 4 + 0])] << 6) \
        + (map_1[ord(old_string[index * 4 + 1])] << 4) \
        + (map_1[ord(old_string[index * 4 + 2])] << 2) \
        + (map_1[ord(old_string[index * 4 + 3])] << 0)])
    return new_string

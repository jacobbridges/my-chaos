import random

#=============
# Key Creators
#=============

def new_major_key():
    list_one, list_two, major_key = range(256), range(256), range(256)
    for index in range(256):
        index_one, index_two = random.randint(0, 255 - index), random.randint(0, 255 - index)
        major_key[index] = list_one[index_one], list_two[index_two]
        del list_one[index_one], list_two[index_two]
    return major_key

def new_minor_key():
    list_one, list_two, minor_key = range(256), range(256), range(256)
    for index in range(256):
        index_one, index_two = random.randint(0, 255 - index), random.randint(0, 255 - index)
        minor_key[index] = list_one[index_one], list_two[index_two] % 4
        del list_one[index_one], list_two[index_two]
    return minor_key

#=====================
# To/From Encoded Keys
#=====================

def new_night_key(major_or_minor_key):
    string = key_to_string(major_or_minor_key)
    string = hide_byte(string)
    string = string_to_code(string)
    string = normalize(string)
    string = hide_word(string)
    string = string_to_code(string)
    return normalize(string)

def new_dream_key(night_key):
    string = clean(night_key)
    string = code_to_string(string)
    string = show_word(string)
    string = clean(string)
    string = code_to_string(string)
    string = show_byte(string)
    return string_to_key(string)

#============================
# new_dream_key()
# These are helper functions.
#============================

def clean(old_string):
    new_string = str()
    for character in old_string:
        if ord(character) != 0:
            new_string += character
    return new_string

def code_to_number(code):
    number = 0
    for character in code:
        number *= 255
        number += ord(character) - 1
    return number

def number_to_string(number):
    string = str()
    while number > 1:
        string = chr(number % 256) + string
        number /= 256
    return string

def code_to_string(code):
    return number_to_string(code_to_number(code))

def show_word(old_string):
    new_string = str()
    for index in range(len(old_string) / 2):
        first, second = ord(old_string[index * 2]), ord(old_string[index * 2 + 1])
        new_string += chr(((first & 0x0F) << 4) + (second >> 4))
    return new_string

def show_byte(old_string):
    new_string = str()
    for index in range(256):
        first, second = ord(old_string[index * 2]), ord(old_string[index * 2 + 1])
        new_string += chr((first & 0xF0) + (second & 0x0F)) + chr(((first & 0x0F) << 4) + (second >> 4))
    return new_string

def string_to_key(string):
    key = range(256)
    for index in range(256):
        key[index] = ord(string[index * 2]), ord(string[index * 2 + 1])
    return key

#============================
# new_night_key()
# These are helper functions.
#============================

def key_to_string(key):
    string = str()
    for first, second in key:
        string += chr(first) + chr(second)
    return string

def hide_byte(old_string):
    new_string = str()
    for index in range(256):
        first, second = ord(old_string[index * 2]), ord(old_string[index * 2 + 1])
        new_string += chr((first & 0xF0) + (second >> 4)) + chr(((second & 0x0F) << 4) + (first & 0x0F))
    return new_string

def string_to_number(string):
    number = 1
    for character in string:
        number *= 256
        number += ord(character)
    return number

def number_to_code(number):
    code = str()
    while number != 0:
        code = chr(number % 255 + 1) + code
        number /= 255
    return code

def string_to_code(string):
    return number_to_code(string_to_number(string))

def normalize(old_string):
    new_string = str()
    for character in old_string:
        while random.randint(0, 255) == 0:
            new_string += chr(0)
        new_string += character
        while random.randint(0, 255) == 0:
            new_string += chr(0)
    return new_string

def hide_word(old_string):
    new_string = str()
    for character in old_string:
        first, second = random.randint(0, 255), ord(character)
        new_string += chr((first & 0xF0) + (second >> 4)) + chr(((second & 0x0F) << 4) + (first & 0x0F))
    return new_string

#==============================
# Key To Quick Key Manipulators
#==============================

def get_left_side(key):
    left_side = range(256)
    for value, index in key:
        left_side[index] = value
    return left_side

def get_right_side(key):
    right_side = range(256)
    for index, value in key:
        right_side[index] = value
    return right_side

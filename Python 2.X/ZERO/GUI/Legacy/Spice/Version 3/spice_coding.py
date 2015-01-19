import progress_bar
import random
import spice_key
import timer

################################################################################

def encode(major_key, minor_key, old_string):
    map_1 = spice_key.get_right_side(major_key)
    map_2 = minor_for_encode(minor_key)
    new_string = str()
    if old_string:
        share = [float(), len(old_string)]
        PB_object, Timer_object = start_progress_bar(share)
        for character in old_string:
            number = map_1[ord(character)]
            new_string += chr(map_2[(number >> 6) & 3][random.randint(0, 63)]) \
            + chr(map_2[(number >> 4) & 3][random.randint(0, 63)]) \
            + chr(map_2[(number >> 2) & 3][random.randint(0, 63)]) \
            + chr(map_2[(number >> 0) & 3][random.randint(0, 63)])
            share[0] += 1
        stop_progress_bar(PB_object, Timer_object)
    return new_string

def decode(major_key, minor_key, old_string):
    map_1 = spice_key.get_right_side(minor_key)
    map_2 = spice_key.get_left_side(major_key)
    new_string = str()
    if old_string:
        share = [float(), len(old_string) / 4]
        PB_object, Timer_object = start_progress_bar(share)
        for index in range(len(old_string) / 4):
            new_string += chr(map_2[(map_1[ord(old_string[index * 4 + 0])] << 6) \
            + (map_1[ord(old_string[index * 4 + 1])] << 4) \
            + (map_1[ord(old_string[index * 4 + 2])] << 2) \
            + (map_1[ord(old_string[index * 4 + 3])] << 0)])
            share[0] += 1
        stop_progress_bar(PB_object, Timer_object)
    return new_string

################################################################################

def minor_for_encode(minor_key):
    map_2 = [[], [], [], []]
    for character, digit in minor_key:
        map_2[digit].append(character)
    return map_2

################################################################################

def start_progress_bar(share):
    PB_object = progress_bar.PB(400, 40)
    Timer_object = timer.Timer(1, update_progress_bar, PB_object, share)
    share.append(Timer_object)
    Timer_object.start()
    return PB_object, Timer_object

def stop_progress_bar(PB_object, Timer_object):
    Timer_object.stop()
    PB_object.close()

def update_progress_bar(PB_object, share):
    try:
        PB_object.update(share[0] / share[1])
    except:
        share[2].stop()

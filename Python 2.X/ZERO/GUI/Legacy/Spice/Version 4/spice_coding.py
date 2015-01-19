import progress_bar
import random
import spice_key
import timer

################################################################################

def encode(major_key, minor_key, source, destination, size):
    map_1 = spice_key.get_right_side(major_key)
    map_2 = minor_for_encode(minor_key)
    if size:
        share = [float(), size]
        PB_object, Timer_object = start_progress_bar(share)
        character = source.read(1)
        while character:
            number = map_1[ord(character)]
            destination.write( \
                chr(map_2[(number >> 6) & 3][random.randint(0, 63)]) + \
                chr(map_2[(number >> 4) & 3][random.randint(0, 63)]) + \
                chr(map_2[(number >> 2) & 3][random.randint(0, 63)]) + \
                chr(map_2[(number >> 0) & 3][random.randint(0, 63)]))
            share[0] += 1
            character = source.read(1)
        stop_progress_bar(PB_object, Timer_object)
    source.close()
    destination.flush()
    destination.close()

def decode(major_key, minor_key, source, destination, size):
    map_1 = spice_key.get_right_side(minor_key)
    map_2 = spice_key.get_left_side(major_key)
    if size:
        share = [float(), size / 4]
        PB_object, Timer_object = start_progress_bar(share)
        dword = source.read(4)
        while dword:
            destination.write(chr(map_2[(map_1[ord(dword[0])] << 6) + \
                                        (map_1[ord(dword[1])] << 4) + \
                                        (map_1[ord(dword[2])] << 2) + \
                                        (map_1[ord(dword[3])] << 0)]))
            share[0] += 1
            dword = source.read(4)
        stop_progress_bar(PB_object, Timer_object)
    source.close()
    destination.flush()
    destination.close()

################################################################################

def minor_for_encode(minor_key):
    map_2 = [[], [], [], []]
    for character, digit in minor_key:
        map_2[digit].append(character)
    return map_2

################################################################################

def start_progress_bar(share):
    PB_object = progress_bar.PB(400, 40)
    Timer_object = timer.Timer(0.1, update_progress_bar, PB_object, share)
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

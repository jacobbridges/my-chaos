import random
MIX = random.SystemRandom().shuffle

def main():
    data = load()
    array = mix(data)
    show(array)

def load():
    while True:
        try:
            filename = raw_input('What file would you like to open? ')
            contents = file(filename, 'rU').read()
            break
        except:
            print 'ERROR: Please try again.'
    array = contents.split('\n')
    data = [[]]
    for line in array:
        if line:
            data[-1].append(line)
        elif data[-1]:
            data.append(list())
    return data

def mix(data):
    array = []
    for group in data:
        array += group
    shuffle(array)
    while group_fail(data, array):
        shuffle(array)
    return array

def shuffle(array):
    print 'Mixing ...',
    MIX(array)
    print 'Done'

def group_fail(groups, array):
    for index, item in enumerate(array):
        index += 1
        for group in groups:
            if item in group:
                if index != len(array) and array[index] in group:
                    print 'ERROR:', array[index-1:index+1]
                    return True
                break
    return False

def show(array):
    print '====================='
    print '       RESULTS       '
    print '====================='
    for line in array:
        print line
    raw_input()

if __name__ == '__main__':
    main()

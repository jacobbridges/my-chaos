#!/usr/bin/python
def main():
    lines = get_lines()
    groups = divide_by_group(lines)
    for index in range(len(groups)):
        group = groups[index]
        names = group[0].split()
        people = process(group)
        for name in names:
            print name, people[name]
        if index + 1 != len(groups):
            print

def get_lines():
    lines = []
    while True:
        line = raw_input()
        try:
            if int(line) == 0:
                return lines
        except:
            pass
        lines.append(line)

def divide_by_group(lines):
    groups = []
    while lines:
        size = int(lines[0]) + 1
        del lines[0]
        groups.append(lines[:size])
        del lines[:size]
    return groups
    
def process(group):
    people = {}
    del group[0]
    for line in group:
        line = line.split()
        people[line[0]] = line[1:]
    money_sent = {}
    for name in people:
        money_sent[name] = 0
    for name in people:
        num_to_give = int(people[name][0])
        num_given = int(people[name][1])
        give_to = people[name][2:]
        try:
            give = num_to_give / num_given
        except:
            give = 0
        for it in give_to:
            money_sent[it] += give
            num_to_give -= give
        money_sent[name] += num_to_give
    net_worth = {}
    for name in people:
        net_worth[name] = money_sent[name] - int(people[name][0])
    return net_worth
            

if __name__ == '__main__':
    main()

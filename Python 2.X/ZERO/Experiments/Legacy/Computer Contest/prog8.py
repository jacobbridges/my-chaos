#!/usr/bin/python
import math

def main():
    data = get_good_input()
    answers = [get_answer(number) for number in data]
    print '\n'.join([str(number) for number in answers])
    
def get_good_input():
    data = []
    while True:
        number = int(raw_input())
        if number:
            data.append(number)
        else:
            return data
        
def get_answer(number):
    return sum([math.log10(number) for number in range(1, number + 1)])
    
if __name__ == '__main__':
    main()

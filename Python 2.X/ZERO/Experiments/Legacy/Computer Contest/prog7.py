#!/usr/bin/python
import math

def main():
    data = get_good_input()
    fiction = get_factorials(data)
    for number in fiction:
        print math.log10(number)
    
def get_good_input():
    data = []
    while True:
        number = int(raw_input())
        if number:
            data.append(number)
        else:
            return data
        
def get_factorials(numbers):
    return [fac(number) for number in numbers]

def fac(number):
    pos = 1
    answer = 1
    while pos <= number:
        answer *= pos
        pos += 1
    return answer

if __name__ == '__main__':
    main()

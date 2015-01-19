#!/usr/bin/python
import math

def main():
    answer = file('answer.txt', 'w')
    # I want 10000 indexs along 2 ** 32.
    requested_indexs = range(0, 2 ** 32, (2 ** 32) / 10000)
    answers = get_answers(requested_indexs)
    string = '[' + ', '.join([str(number) for number in answers]) + ']'
    answer.write(string)
    answer.close()
    
def get_answers(indexs):
    answers = [None]
    del indexs[0]
    pos = 1
    answer = 0
    while indexs:
        answer += math.log10(pos)
        if pos == indexs[0]:
            del indexs[0]
            answers.append(answer)
            print answer
        pos += 1
    
if __name__ == '__main__':
    main()

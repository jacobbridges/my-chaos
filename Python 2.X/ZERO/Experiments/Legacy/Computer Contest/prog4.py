#!/usr/bin/python
def main():
    problem_set = [18, 33, 44]
    print sum(get_fibonacci_on_index(problem_set))
    
def get_fibonacci_on_index(indexs):
    indexs = sorted([abs(int(index)) for index in indexs if abs(int(index)) != 0])
    fibonacci_numbers = [1, 1]
    answers = []
    current_index = 1
    while indexs:
        if current_index == indexs[0]:
            answers.append(fibonacci_numbers[current_index - 1])
            del indexs[0]
        else:
            current_index += 1
            if current_index > len(fibonacci_numbers):
                fibonacci_numbers.append(fibonacci_numbers[-2] + fibonacci_numbers[-1])
    return answers
    
if __name__ == '__main__':
    main()

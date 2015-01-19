def main():
    string = get_input()
    test_cases = parse_input(string)
    cast_cases(test_cases)
    check_cases(test_cases)
    answers = process_cases(test_cases)
    show_answers(answers)

def get_input():
    string = ''
    while True:
        try:
            line = raw_input()
            if line == '0 0 0 0':
                return string[:-1]
            else:
                string += line + '\n'
        except:
            return string[:-1]

def parse_input(string):
    test_cases = string.splitlines()
    for index in range(len(test_cases)):
        test_cases[index] = test_cases[index].split()
    return test_cases

def cast_cases(test_cases):
    for index in range(len(test_cases)):
        a, b, c, d = test_cases[index]
        test_cases[index] = int(a), int(b), int(c), int(d)

def check_cases(test_cases):
    for test_case in test_cases:
        for number in test_case:
            if not 0 <= number <= 39:
                raise 'ERROR' + str(test_case)

def process_cases(test_cases):
    answers = []
    for test_case in test_cases:
        answers.append(calculate(test_case))
    return answers

def calculate(test_case):
    current_mark = test_case[0]
    total_marks = 0
    # calculate step 1
    current_mark = current_mark
    total_marks += 80
    # calculate step 2
    while current_mark != test_case[1]:
        current_mark -= 1
        if current_mark < 0:
            current_mark = 39
        total_marks += 1
    # calculate step 3
    current_mark = current_mark
    total_marks += 40
    # calculate step 4
    while current_mark != test_case[2]:
        current_mark += 1
        if current_mark > 39:
            current_mark = 0
        total_marks += 1
    # calculate step 5
    while current_mark != test_case[3]:
        current_mark -= 1
        if current_mark < 0:
            current_mark = 39
        total_marks += 1
    # convert "total_marks" to degrees and return
    return total_marks * 9

def show_answers(answers):
    for answer in answers:
        print answer

if __name__ == '__main__':
    main()

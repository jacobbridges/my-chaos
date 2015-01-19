#!/usr/bin/python
def main():
    all_input = get_all_input()
    codes_found = find_codes(all_input)
    missing_codes = find_missing_codes(codes_found, 32, 122)
    print ''.join([chr(code) for code in missing_codes])
    
def get_all_input():
    string = ''
    while True:
        try:
            string += raw_input()
        except:
            return string
        
def find_codes(string):
    return [ord(character) for character in string]

def find_missing_codes(codes, low, high, step=1):
    if low > high:
        low, high = high, low
    answers = []
    for code in range(low, high + step, step):
        if code not in codes:
            answers.append(code)
    return answers

if __name__ == '__main__':
    main()

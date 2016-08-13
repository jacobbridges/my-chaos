# Create a mapping of letters to numbers
lower_alpha = 'abcdefghijklmnopqrstuvwxyz'
lower_dictn = {k+1: v for k, v in enumerate((lower_alpha))}
lower_dicta = {v: k for k, v in lower_dictn.items()}


# Functions

def make_cypher(letter):
    """Make a new mapping for any letter (circular letter)."""
    idx = lower_dicta[letter]
    return {k: lower_dictn[(v - idx + 27) if (v - idx + 1) <= 0 else (v - idx + 1)] for k, v in lower_dicta.items()}


def rotating_encrypter(string, key):
    """Encrypt a string one word at a time with a rotating encryption based on the key."""
    string = string.lower()
    new_string = []
    cyphers = [make_cypher(l) for l in key]
    keylen = len(key)
    for word in string.split(' '):
        new_word = ''
        for i, l in enumerate(word):
            if l in cyphers[i % keylen]:
                new_word += cyphers[i % keylen][l]
            else:
                new_word += l
        new_string.append(new_word)
    return ' '.join(new_string)


# Main Function

def main():
    import sys
    print rotating_encrypter(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()



import random, sys

NAMES = sorted('''\
Chris Hansen
Adam Cox
Micah Hocson
Stephen Chappell
Jonathan Ballou
Joshua Lovegrove
James Carnicle'''.split('\n'))

for debtor in NAMES:
    sys.stdout.write(debtor + '\n')
    for creditor in sorted(random.sample(NAMES, random.randint(2, len(NAMES)))):
        if creditor != debtor:
            sys.stdout.write(creditor + '\n')
            value = str(random.randint(100, 2000))
            sys.stdout.write(value + '\n')
    sys.stdout.write('\n')
sys.stdout.write('\n')

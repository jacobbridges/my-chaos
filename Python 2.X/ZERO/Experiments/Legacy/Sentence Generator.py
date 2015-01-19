import random

# PART 1

shuffled = []
pronoun = ['he', 'she', 'it', 'who', 'what']
verb = ['lives', 'plays', 'dies', 'rises', 'eats']
adverb = ['joyfully', 'excitedly', 'sadly', 'suddenly', 'harshly']
preposition = ['on', 'with', 'in', 'besides', 'under']
adjective = ['his', 'her', 'my', 'the', 'a']
description = ['silly', 'firey', 'sickening', 'rainbow', 'shocking']
noun = ['house', 'sand', 'grave', 'elephant', 'boot']

sentences = [' '.join((pro.capitalize(), ver, adv, pre, adj, des, nou)) + \
             ('?' if pro in ('who', 'what') else '.') \
             for pro in pronoun for ver in verb for adv in adverb \
             for pre in preposition for adj in adjective \
             for des in description for nou in noun]

while sentences:
    index = random.randint(0, len(sentences) - 1)
    shuffled.append(sentences[index])
    del sentences[index]

file('Group 1.txt', 'w').write('\n'.join(shuffled))

# PART 2

shuffled = []
names = ['Adam', 'Eve', 'Cain', 'Abel', 'Seth']
verbs = ['lived', 'died', 'woke', 'slept', 'ate']
adverbs = ['well', 'poorly', 'happily', 'mournfully', 'quickly']
prepositions = ['in', 'on', 'with', 'beside', 'for']
adjectives = ['his', 'her', 'my', 'its', 'the']
nouns = ['animals', 'children', 'cities', 'plants', 'buildings']

sentences = [' '.join((name,  verb, adverb, preposition, adjective, noun)) + '.' \
             for name in names for verb in verbs for adverb in adverbs \
                 for preposition in prepositions for adjective in adjectives for noun in nouns]

length = len(sentences)
for index_1 in range(length):
    index_2 = random.randint(0, length - 1 - index_1)
    shuffled.append(sentences[index_2])
    del sentences[index_2]

file('Group 2.txt', 'w').write('\n'.join(shuffled))

# PART 3

shuffled = []
names = ['Matthew', 'Mark', 'Luke', 'John', 'James', 'Jude', 'Samuel',
         'David', 'Job', 'Jacob', 'Abel', 'Joshua', 'Joseph', 'Aaron',
         'Paul', 'Jonah', 'Jonathan', 'Amos', 'Peter', 'Stephen',
         'Barnabus', 'Solomon', 'Christian', 'Joy', 'Love', 'Peace',
         'Longsuffering', 'Gentleness', 'Goodness', 'Faith', 'Meekness',
         'Temperance', 'Michael', 'Gabriel']

sentences = [' '.join((first, 'is the bother of', second)) + '.' \
             for first in names for second in names if first != second]

length = len(sentences)
for index_1 in range(length):
    index_2 = random.randint(0, length - index_1 - 1)
    shuffled.append(sentences[index_2])
    del sentences[index_2]
    
file('Group 3.txt', 'w').write('\n'.join(shuffled))

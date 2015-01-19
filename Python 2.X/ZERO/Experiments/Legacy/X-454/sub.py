dictionary = {'Lamb': 'Sacrifice', 'Emmanuel': 'NovaSuperNova', ' heaven': ' the Pyramid of Dragons', ' the earth': ' Neopia', ' by man': ' by one', 'Christ': 'the Everlasting Light', " potter's vessel": ' clay pot', ' slain': ' destroyed', 'God': 'Zero', ' a man of sorrows': ' being of sorrows', ' the world': ' Neopia', ' our Lord': ' Zero', ' his own way': ' a lost path', 'Saviour': 'Hero', 'The Lord': 'NovaSuperNova', ' this world': ' Neopia', ' worms': ' death', ' wounded': ' torn', ' begotten': ' sired', ' gospel': ' message', ' a virgin shall conceive and bear a Son': ' a child shall bear a Son', ' preach': ' serve', 'Zion': 'the Garden Of Dragons', 'Gentiles': 'Barbarians', ' the sons of Levi': ' the sons of Qasala', ' dash': ' break', ' heavenly host': ' Atlantian dragons', ' my flesh': ' my body', ' no man': ' no one', 'King of Glory': 'Lord of Sand', ' angels': ' messengers', ' the Lord God': ' the Three', ' worship': ' love and adore', ' gone astray': ' lost the way', ' iniquity': ' unrighteousness', ' the Lord of Hosts': ' the King of the Desert', ' tidings': ' news', ' that sleep': ' that are dead', ' smiters': ' evil ones', ' in hell': ' with Jhudora', ' makes intercession for': ' defends', ' iniquities': ' wrongdoings', 'His Christ': 'the Everlasting Light', ' at the latter day': ' in the future', 'Thou suffer Thy': 'Thou allow Thy', 'His Anointed': 'His Crown', ' chastisement': ' punishment', ' derision': ' ridicule', ' preachers': ' servants', ' the Lord': ' NovaSuperNova', ' our God': ' Zero', ' my people': ' the dragons', 'Hallelujah': 'Excellence', ' heathen': ' barbarians', ' the King of Glory': ' the King of the Desert', ' city of David': ' city of Coltzan', ' sin': ' evil', ' your God': ' Zero', ' angel': ' messenger', ' stricken': ' struck', ' stripes': ' scars', 'Lord Jesus Christ': 'Lord NovaSuperNova', ' transgressions': ' shortcomings', 'Redeemer': 'Hero', ' cities of Judah': ' city of Sakhmet', ' men': ' Neopians', ' bruised': ' beaten', ' first fruits': ' first gathering', 'Lamb of God': 'Sacrifice of Zero', 'Christ the Lord': 'the Everlasting Light', 'Wonderful, Counsellor, the Mighty God, the Everlasting Father, the Prince of Peace': 'Remarkable, Adviser, the Powerful One, the Constant Father, the Prince of the Desert', 'The Lord of Hosts': 'Zero', 'Jerusalem': 'the City Of Peace', 'GOD WITH US': 'THE EVERLASTING LIGHT', 'Adam': 'Sloth'}

# A Project To Convert The Messiah For Use By NovaSuperNova
# =========================================================
# It may to likened to apples of silver in pictures of bronze.
# The results are meant to be symbols of God and pointers to our Savior.
# Please do not misunderstand that nature and purpose of this project.

def cmp(x, y):
    if len(x) > len(y):
        return -1
    elif len(x) < len(y):
        return 1
    else:
        return 0

keys = dictionary.keys()
keys.sort(cmp)

converted = file('M Part 3V1.txt', 'rb', 0).read()

for key in keys:
    converted = converted.replace(key, dictionary[key])

file('M Part 3V3.txt', 'wb', 0).write(converted)

manual = file('M Part 3V2.txt', 'rb', 0).read()

print converted == manual
if not converted == manual:
    print 'len(converted) =', len(converted)
    print 'len(manual) =', len(manual)
    for index in range(len(manual)):
        if converted[index] != manual[index]:
            print 'index =', index
            break
    print 'converted =', converted[index-20:index+20]
    print 'manual =', manual[index-20:index+20]

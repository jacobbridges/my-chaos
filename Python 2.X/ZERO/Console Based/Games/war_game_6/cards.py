import Zpaw

# Card definitions are simpler that before.
card_0 = Zpaw.page(5, 5).mutate(0, 0, '+---+').mutate(1, 0, '|   |').mutate(2, 0, '| 0 |').mutate(3, 0, '|   |').mutate(4, 0, '+---+')
card_1 = Zpaw.page(0, 0).link(card_0).unlink().mutate(2, 2, '1')
card_2 = Zpaw.page(0, 0).link(card_0).unlink().mutate(2, 2, '2')
card_3 = Zpaw.page(0, 0).link(card_0).unlink().mutate(2, 2, '3')
card_4 = Zpaw.page(0, 0).link(card_0).unlink().mutate(2, 2, '4')
card_5 = Zpaw.page(0, 0).link(card_0).unlink().mutate(2, 2, '5')
card_6 = Zpaw.page(0, 0).link(card_0).unlink().mutate(2, 2, '6')
card_7 = Zpaw.page(0, 0).link(card_0).unlink().mutate(2, 2, '7')
card_8 = Zpaw.page(0, 0).link(card_0).unlink().mutate(2, 2, '8')
card_9 = Zpaw.page(0, 0).link(card_0).unlink().mutate(2, 2, '9')
card_10 = Zpaw.page(0, 0).link(card_0).unlink().mutate(2, 1, '1 0')
card_A = Zpaw.page(0, 0).link(card_0).unlink().mutate(2, 2, 'A')
card_J = Zpaw.page(0, 0).link(card_0).unlink().mutate(2, 2, 'J')
card_Q = Zpaw.page(0, 0).link(card_0).unlink().mutate(2, 2, 'Q')
card_K = Zpaw.page(0, 0).link(card_0).unlink().mutate(2, 2, 'K')

# Test what the cards look like.
def main():
    print card_0
    print card_1
    print card_2
    print card_3
    print card_4
    print card_5
    print card_6
    print card_7
    print card_8
    print card_9
    print card_10
    print card_A
    print card_J
    print card_Q
    print card_K

# Test this module.
if __name__ == '__main__':
    main()

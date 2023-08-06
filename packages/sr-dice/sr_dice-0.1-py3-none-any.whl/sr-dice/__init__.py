
import argparse
import secrets

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rolls D6 and evaluates the results for Shadowrun.')
    parser.add_argument('num_dices', type=int, help='number of dices to roll')
    parser.add_argument('--hist', help='print a histogram of the dice rolls',
                        action='store_const', const=True, default=False,)
    parser.add_argument('--raw', help='print the raw dice rolls',
                        action='store_const', const=True, default=False,)
    args = parser.parse_args()
    num_dices = args.num_dices

    if num_dices < 1:
        parser.error('num_dices must be positive integer')

    hits = 0
    misses = 0
    rolls_hist = [0] * 6
    rolls_str = ''
    for i in range(num_dices):
        roll = secrets.choice([1, 2, 3, 4, 5, 6])
        hits += roll >= 5
        misses += roll == 1
        rolls_hist[roll - 1] += 1
        rolls_str += str(roll) + ' '

    print()
    print(' {:<12}  {:}'.format('Hits:', hits))
    print(' {:<12}  {:}'.format('Misses:', misses))
    print()

    if misses > num_dices/2.:
        if hits == 0:
            print(' CRITICAL GLITCH')
        else:
            print(' GLITCH')
        print()

    if args.hist:
        print(' {:<12}  1 | 2 | 3 | 4 | 5 | 6 '.format('Histogram:'))
        print(' {:<12} {:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}'.
              format('', rolls_hist[0], rolls_hist[1], rolls_hist[2],
                     rolls_hist[3], rolls_hist[4], rolls_hist[5]))
        print()

    if args.raw:
        print(' {:<12}  {:}'.format('Dice rolls:', rolls_str))
        print()

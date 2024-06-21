#!/usr/bin/python3
import re
from numberutils import factorize_by_trial_division
from donumbers import do_numbers

ROUNDS = (([9, 1, 4, 2, 9, 1], 273),
          ([75, 25, 50, 100, 7, 3], 431),
          ([50, 5, 1, 9, 8, 1], 571),
          ([100, 75, 25, 50, 10, 9], 882),
          ([25, 1, 1, 2, 4, 3], 525),
          ([25, 75, 100, 3, 2, 2], 669),
          ([100, 50, 75, 25, 2, 5], 903),
          ([25, 1, 5, 5, 4, 3], 993))

if __name__ == '__main__':
    for round in ROUNDS:
        print('')
        answer = ''
        numbers = round[0]
        target = round[1]
        print('Numbers:', numbers)
        print('Target:',target)
        factors = factorize_by_trial_division(target)
        if not factors:
            print(target, "is prime")
            continue
        used = []
        for f in factors:
            if f in used:
                continue
            nos = numbers.copy()
            r1 = do_numbers(nos, f, 0, limit=2, silent=True)
            if r1:
                l = re.findall(r'\d+', r1[0])       # unpack returned expression into number list
                for n in l:
                    nos.remove(int(n))
                multiplier = target // f            # factor * multiplier = target
                r2 = do_numbers(nos, multiplier, 0, limit=2, silent=True)
                if r2:
                    answer = '(' + r2[0] + ')*(' + r1[0] + ')'
                used.append(f)
                used.append(multiplier)
            if answer:
                print('Answer:', answer)
                break
        if not answer:
            print("No answer")
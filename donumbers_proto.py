#!/usr/bin/python3
import math
import random
from itertools import permutations
from numberutils import factorize_by_trial_division

def factorize_using_local_list(n: int, l: list[int] ) -> list[tuple]:
    """ Return a list of the best fit factors for a natural number based on an input list.
        Returns:  factor, multiplier, result and remainder """
    a = []                              # Empty list
    l_iter = iter(l)
    while True:
        try:
            f = next(l_iter)
            r = int(math.remainder(n, f))   # Remainder
            if r >= 0:
                m = n // f                  # Multiplier 1
            else:
                m = (n + f) // f            # Multiplier 2
            a.append(((f, m, m * f, r)))
        except StopIteration: 
            break                  
    return a

def get_results(l:list[int]) -> list[tuple[int]]:
    res = []
    for i in permutations(l, 2):
        print("+", i[0], i[1], i[0] + i[1])
        print("-", i[0], i[1], i[0] - i[1])
        print("*", i[0], i[1], i[0] * i[1])
        if i[0] % i[1] == 0: print("/", i[0], i[1], i[0] // i[1])
    return res

if __name__ == '__main__':
    while True:
        large_numbers = [25, 50, 75, 100]
        number_list = []
        numbers = input("Enter your numbers: ").strip().lower()
        if numbers == "quit" or numbers == "exit":
            break
        if not numbers:
            lrg = random.randint(1, 4)
            sml = 6 - lrg
            while lrg > 0:
                l = len(large_numbers) - 1
                x = large_numbers[random.randint(0,l)]
                number_list.append(x)
                large_numbers.remove(x)
                lrg-= 1
            while sml > 0:
                number_list.append(random.randint(1, 10))
                sml-= 1
            numbers = " ".join(str(x) for x in number_list)
        else:
            try:
                number_list = [int(x) for x in numbers.split(" ")]
            except:
                continue
        if len(number_list) != 6:
            continue
        print(numbers)
        while True:
            target = input("Enter your target: ").strip()
            if not target:
                target = random.randint(100, 999)
            else:
                try:
                    target = int(target)
                    if target < 100:
                        continue
                except:
                    continue
            break
        print("Target:", target)
        factors = factorize_by_trial_division(target)
        if len(factors) == 0:
            msg = str(target) + " is prime!"
        else:
            msg = ""
        print("Prime factors:", factors, msg)
        factors = sorted(factorize_using_local_list(target, number_list), 
                         key=lambda facs: abs(facs[3]))
        print("Best factors:", factors)
        print("Possible solutions:")
        for f in factors:
            if f[1] in number_list or abs(f[3]) in number_list:
                print(f)
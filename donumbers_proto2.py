#!/usr/bin/python3
import random
import time
import warnings
from donumbers import format_solution
from donumbers import crunch_numbers
from donumbers import strip_numbers
from donumbers import do_rough_factorization
from donumbers import LARGE_NUMBERS

if __name__ == '__main__':
    warnings.filterwarnings('error')
    while True:
        large_numbers = LARGE_NUMBERS.copy()
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
        print("Numbers:", numbers)
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
        starttime = time.time()
        solutions = do_rough_factorization(number_list, target, debug=True)
        currenttime = time.time()
        print("Execution:", int(currenttime-starttime), "seconds")
        print(format_solution(solutions))
#!/usr/bin/python3
import random
import time
import warnings
from donumbers import numbers_main_sync
from donumbers import get_some_numbers
from donumbers import format_solution

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    i = 0
    autofile = str(int(time.time()))
    while i < 100:
        # do lots of tests and report those that don't meet target or take too long
        (numbers, _) = get_some_numbers()
        target = random.randint(100, 999)
        (time_taken, solutions) = numbers_main_sync(numbers, target, True, autofile)
        if time_taken > 30 or eval(solutions[0]) != target:
            print("Numbers:", numbers, "Target:", target, "Time:", time_taken, "Best:", format_solution(solutions))
        i+= 1

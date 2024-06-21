#!/usr/bin/python3
import random
import re
import time
from itertools import permutations
from itertools import product
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed

def rebuild_expression(expr: str, tokens: list[tuple]) -> str:
    expression = expr
    tokens.reverse()
    for t in tokens:
        expression = expression.replace(t[0], "(" + t[1] + ")", 1)
    return expression

def evaluate_conventional(expression: str, target: int, variance: int) ->  tuple:
    ''' 
    Evaluate an expression using conventional operator precedence (*, /, +, -)
    '''
    res = ()
    try:
        r = eval(expression)
        diff = target - r
        if diff == int(diff) and abs(diff) <= variance:
            res = (expression, int(r), int(diff))
            if diff == 0:
                return res      # Return an exact match
    except ZeroDivisionError:
        pass

    return res

def evaluate_in_order(expression: str, target: int, variance: int) -> tuple:
    ''' 
    Evaluate an expression in order of terms
    '''
    tokens = []
    res = ()
    while True:
        r = re.search(r'\d+[\+\-\*\/]\d+', expression)
        if r:
            g = r.group()
            try:
                r = eval(g)
                int_r = int(r)
                if int_r == r:
                    s = str(int_r)
                    tokens.append((s, g))
                    expression = expression.replace(g, s, 1)
                    try:
                        r = eval(expression)
                        diff = target - int_r
                        if r == int_r and abs(diff) <= variance:
                            expression2 = rebuild_expression(expression, tokens)    # explain workings
                            if res:
                                if abs(diff) < abs(res[2]): 
                                    res = (expression2, int_r, diff)
                            else:
                                res = (expression2, int_r, diff)
                            if diff == 0:
                                return res
                    except:
                        continue
                else:
                    break
            except:
                break
        else:
            break

    return res

def evaluate_with_parenthesis(expression:str, target:int, variance:int) -> tuple:
    # Evaluate an expression by subdividing with parenthesis
    res = ()
    expression_sav = expression
    r = re.findall(r'[\+\-\*\/]\d+',expression)
    expression = expression.replace(r[0], r[0]+')', 1)
    expression = '(' + expression
    try:
        v = eval(expression)
        diff = target - v
        if int(diff) == diff and abs(diff) <= variance:
            res = (expression, int(v), int(diff))
            if diff == 0:
                return res
    except:
        pass
    expression = expression_sav
    for x in r:
        expression = expression.replace(x, x[0]+'('+x[1:], 1)
        expression+= ')'
        ex2 = re.search(r'\([\d\+\-\/\*]+\)', expression)
        r2 = eval(ex2.group())          # eliminate fractions
        if r2 == int(r2):
            try:
                r = eval(expression)
                diff = target - r
                if int(diff) == diff and abs(diff) <= variance:
                    if res:
                        if abs(diff) < abs(res[2]): 
                            res = (expression, int(r), int(diff))
                    else:
                        res = (expression, int(r), int(diff))
                    if diff == 0:
                        return res
            except:
                continue
        expression = expression_sav
    return res

def evaluate_switching_precedence(expression: str, target: int, variance: int) -> tuple:
    ''' 
    Evaluate switching precedence to (+, -, *, /) by doing addition and subtraction first
    '''
    tokens = []
    res = ()
    while True:
        r = re.search(r'\d+[\+\-]\d+',expression)
        if r:
            g = r.group()
            s = str(eval(g))
            tokens.append((s, g))
            expression = expression.replace(g, s, 1)
            try:
                r = eval(expression)
                diff = target - r
                if diff == int(diff) and abs(diff) <= variance:
                    expression2 = rebuild_expression(expression, tokens)    # explain workings
                    if res:
                        if abs(diff) < abs(res[2]): 
                            res = (expression2, int(r), int(diff))
                    else:
                        res = (expression2, int(r), int(diff))
                    if diff == 0:
                        return res
            except:
                continue
        else:
            break

    return res

def do_numbers(nos:list[int], target:int, variance:int, limit:int=30) -> list[tuple[int]]:
    ''' 
    Find a target number within variance by applying the mathematical operators
    supplied (+, -, * or /) on a list of numbers provided (note that each number 
    can only be used once).
    '''
    OPERATIONS = ("+", "-", "*", "/")
    res = ()
    noslen = len(nos)
    i = 2
    starttime = time.time()
    with ProcessPoolExecutor(4) as executor:
        while i <= noslen:            
            currenttime = time.time()
            # Timeout, return best answer
            if currenttime - starttime > (limit-1):
                print("Timeout warning!")
                print(res)

            # Brute force our way through mathematical expressions
            # made from all permutations of numbers and operators
            j = 1
            opslist = []
            while j < i:
                opslist.append(OPERATIONS)
                j+= 1
            operators = tuple(product(*opslist))
            for n in permutations(nos, i):                
                for o in operators:
                    expression = ""
                    j = 0
                    olim = len(o)
                    while j < len(n):   # Make the arithmetic expression
                        expression+= str(n[j])
                        if j < olim:
                            expression+= o[j]
                        j+= 1

                    '''
                    # Evaluate expression using conventional operator precedence (*, /, +, -)
                    res = evaluate_conventional(expression, target, variance)
                    if res and res[2] == 0:
                        return res

                    # If that didn't work evaluate expression in order of appearance
                    res2 = evaluate_in_order(expression, target, variance)
                    if res2 and res2[2] == 0:
                        return res2
                    if res2:
                        if not res:
                            res = res2
                        elif abs(res2[2]) < abs(res[2]):
                            res = res2

                    # If that didn't work didn't try parenthesis
                    res2 = evaluate_with_parenthesis(expression, target, variance)
                    if res2 and res2[2] == 0:
                        return res2
                    if res2:
                        if not res:
                            res = res2
                        elif abs(res2[2]) < abs(res[2]):
                            res = res2

                    # If that didn't work switch precedence to (+, -, *, /) by evaluating 
                    # addition and subtraction first
                    res2 = evaluate_switching_precedence(expression, target, variance)
                    if res2 and res2[2] == 0:
                        return res2
                    if res2:
                        if not res:
                            res = res2
                        elif abs(res2[2]) < abs(res[2]):
                            res = res2
                    '''

                    # submit tasks and collect futures
                    futures = [executor.submit(evaluate_conventional, expression, target, variance),
                                executor.submit(evaluate_in_order, expression, target, variance),
                                executor.submit(evaluate_with_parenthesis, expression, target, variance),
                                executor.submit(evaluate_switching_precedence, expression, target, variance)]
                    # process task results as they are available
                    for future in as_completed(futures):
                        # retrieve the result
                        res2 = future.result()
                        if res2 and res2[2] == 0:
                            return res2
                        if res2:
                            if not res:
                                res = res2
                            elif abs(res2[2]) < abs(res[2]):
                                res = res2
                    
            i+= 1
    
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
        solutions = do_numbers(number_list, target, 10)
        currenttime = time.time()
        print("Execution:", int(currenttime-starttime), "seconds")
        print(solutions)
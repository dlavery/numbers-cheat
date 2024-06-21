#!/usr/bin/python3
import math
import random
import re
from itertools import permutations
from itertools import product

def rebuild_expression(expr: str, tokens: list[tuple]) -> str:
    expression = expr
    tokens.reverse()
    for t in tokens:
        expression = expression.replace(t[0], "(" + t[1] + ")", 1)
    return expression

if __name__ == '__main__':
    while True:
        expression = input("Enter your expression: ").strip().lower()
        if expression == "quit" or expression == "exit":
            break
        print(expression)
        expression_sav = expression
        tokens = []
        target = 882
        expression_sav = expression
        while True:
            r = re.search(r'\d+[\+\-\*\/]\d+', expression)
            if r:
                g = r.group()
                try:
                    r = eval(g)
                    if r == int(r):
                        s = str(int(r))
                        tokens.append((s, g))
                        expression = expression.replace(g, s, 1) # explain workings
                    else:
                        break
                except:
                    continue
            else:
                break
        print(expression)
        res = ()
        try:
            r = eval(expression)
            int_r = int(r)
            diff = target - int_r
            if r == int_r and abs(diff) <= 10:
                expression2 = rebuild_expression(expression, tokens)    # explain workings
                if res:
                    if abs(diff) < abs(res[2]): 
                        res = (expression2, int_r, diff)
                else:
                    res = (expression2, int_r, diff)
                if diff == 0:
                    print("Success:", res)
        except:
            continue
        print(res)
        expression = expression_sav

        # If that didn't work didn't try parenthesis
        expression_sav = expression
        r = re.findall(r'[\+\-\*\/]\d+',expression)
        for x in r:
            print(x)
            expression = expression.replace(x, x[0]+'('+x[1:], 1)
            expression+= ')'
            print(expression)
            try:
                r = eval(expression)
                int_r = int(r)
                diff = target - int_r
                if r == int_r and abs(diff) <= 10:
                    if res:
                        if abs(diff) < abs(res[2]): 
                            res = (expression, int_r, diff)
                    else:
                        res = (expression, int_r, diff)
                    if diff == 0:
                        print("Success:", res)
            except:
                continue
            expression = expression_sav
        print(res)

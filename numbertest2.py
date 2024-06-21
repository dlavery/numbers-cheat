#!/usr/bin/python3

import re
import warnings
from donumbers import evaluate_with_parenthesis
from donumbers import evaluate_switching_precedence
from donumbers import evaluate_conventional
from donumbers import evaluate_in_order
from donumbers import crunch_numbers
from donumbers import make_up_difference
from donumbers import rebuild_expression
from donumbers import make_up_difference
from donumbers import LARGE_NUMBERS
from donumbers import strip_numbers
from donumbers import do_rough_rough_factorization
from donumbers import do_small_factorization
from donumbers import do_numbers
from donumbers import apply_brackets
from donumbers import do_split
from donumbers import complement
from itertools import combinations
from itertools import product

def evaluate_recursively():
    pass

def do_3_3_split(numbers:list[int], target:int, debug:bool=False) -> tuple:
    ''' Split 6 numbers into 2 groups equally and try to make the target '''
    OPERATIONS = ("+", "-", "*", "/")
    j = 1
    opslist = []
    while j < 3:
        opslist.append(OPERATIONS)
        j+= 1
    operators = tuple(product(*opslist))
    for c in combinations(numbers, 3):
        c_ = complement(numbers, c)
        expressions = []
        for o in operators:
            expression = ""
            j = 0
            olim = len(o)
            while j < len(c):   # Make the arithmetic expression
                expression+= str(c[j])
                if j < olim:
                    expression+= o[j]
                j+= 1
            expressions.append(expression)
            try:
                eval_expression = eval(expression)
                for e in apply_brackets(expression):
                    if eval(e) != eval_expression:
                        expressions.append(e)
            except ZeroDivisionError:
                continue
        for e in expressions:
            try:
                v = eval(e)
                if v != int(v):
                    continue
                if v < target:
                    q = target // v
                    soln = do_numbers(list(c_), q, 0, True)
                    if soln:
                        e2 = "(" + e + ")*(" + soln[0] + ")"
                        if eval(e2) == target:
                            return (e2, target, 0)
                    add = target - v
                    soln = do_numbers(list(c_), add, 0, True)
                    if soln:
                        return ("(" + e + ")+(" + soln[0] + ")", target, 0)
                elif v > target:
                    m = v // target
                    soln = do_numbers(list(c_), m, 0, True)
                    if soln:
                        e2 = "(" + e + ")/(" + soln[0] + ")"
                        if eval(e2) == target:
                            return (e2, target, 0)
                    sub = v - target
                    soln = do_numbers(list(c_), sub, 0, True)
                    if soln:
                        return ("(" + e + ")-(" + soln[0] + ")", target, 0)
                else:
                    return (e, target, 0)
            except ZeroDivisionError:
                continue
    return ()

def do_4_2_split(numbers:list[int], target:int, debug:bool=False) -> tuple:
    ''' Split 6 numbers into 2 groups of 4 and 2 and try to make the target '''
    OPERATIONS = ("+", "-", "*", "/")
    j = 1
    opslist = []
    while j < 4:
        opslist.append(OPERATIONS)
        j+= 1
    operators = tuple(product(*opslist))
    for c in combinations(numbers, 4):
        c_ = complement(numbers, c)
        expressions = []
        for o in operators:
            expression = ""
            j = 0
            olim = len(o)
            while j < len(c):   # Make the arithmetic expression
                expression+= str(c[j])
                if j < olim:
                    expression+= o[j]
                j+= 1
            expressions.append(expression)
            try:
                eval_expression = eval(expression)
                for e in apply_brackets(expression):
                    if eval(e) != eval_expression:
                        expressions.append(e)
            except ZeroDivisionError:
                continue
        for e in expressions:
            try:
                v = eval(e)
                if v != int(v):
                    continue
                if v < target:
                    q = target // v
                    soln = do_numbers(list(c_), q, 0, True)
                    if soln:
                        e2 = "(" + e + ")*(" + soln[0] + ")"
                        if eval(e2) == target:
                            return (e2, target, 0)
                    add = target - v
                    soln = do_numbers(list(c_), add, 0, True)
                    if soln:
                        return ("(" + e + ")+(" + soln[0] + ")", target, 0)
                elif v > target:
                    m = v // target
                    soln = do_numbers(list(c_), m, 0, True)
                    if soln:
                        e2 = "(" + e + ")/(" + soln[0] + ")"
                        if eval(e2) == target:
                            return (e2, target, 0)
                    sub = v - target
                    soln = do_numbers(list(c_), sub, 0, True)
                    if soln:
                        return ("(" + e + ")-(" + soln[0] + ")", target, 0)
                else:
                    return (e, target, 0)
            except ZeroDivisionError:
                continue
    return ()

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    '''print('evaluate_with_parenthesis', evaluate_with_parenthesis('25*5*5+3', 993, 100))
    print('evaluate_switching_precedence', evaluate_switching_precedence('25*5*5+3', 993, 100))
    print('evaluate_conventional', evaluate_conventional('25*5*5+3', 993, 100))
    print('evaluate_in_order', evaluate_in_order('25*5*5+3', 993, 100))

    print('output:', crunch_numbers([25,1,5,5,4,3],4,993,100))'''

    #print(make_up_difference(632, ('25*5*5', 625, 7),[3,2,4]))
    #print(make_up_difference(632, ('25*5', 125, 507),[6,3,2,4]))

    #print('output:', crunch_numbers([25,7,4,1,1],5,814,100))
    #print('output:', crunch_numbers([25,7,4,1,1,6],2,8,0))
    #print('output:', crunch_numbers([25,4,1,6],1,6,6))
    #print('output:', crunch_numbers([25,4,1],3,101,0))

    '''
    fres = (crunch_numbers([75, 4, 4, 8], x+1, 2, 0) for x in range(3))
    for f in fres:
        print(f)
    '''
    '''print(make_up_difference(602, ('6*100', 600, 2), [1, 10, 4, 8]))
    print(make_up_difference(602, ('6*100', 600, 2), [1, 10, 2, 3]))
    print(make_up_difference(598, ('6*100', 600, -2), [1, 10, 2, 3]))
    print(make_up_difference(602, ('6*100', 600, 17), [1, 10, 1, 1]))'''

    #print('output:', crunch_numbers([50,5,1,9,8,1],5,571,100,debug=True))

    #print('output:', rebuild_expression('57*10',[('57', '49+8') ,('49', '50-1'), ('10', '9+1')], 571, True))
    #print('output:', rebuild_expression('57*10',[('49', '50-1'), ('57', '49+8'), ('10', '9+1')], 571, True))
    
    #print('evaluate_switching_precedence', evaluate_switching_precedence('50-1+8*9+1', 571, 100, debug=True))

    '''print(224, make_up_difference(('2*100', 200, 24), [8,2,9,6]))                   # 224
    print(224, make_up_difference(('2*100', 200, 24), [7,2,9,1], variance=True))    # 224
    print(176, make_up_difference(('2*100', 200, -24), [7,2,9,1], variance=True))   # 176 
    print(187, make_up_difference(('2*100', 200, -13), [7,2,9,9], variance=True))   # 187
    print(213, make_up_difference(('2*100', 200, 13), [7,2,9,9], variance=True))    # 213
    print(616, make_up_difference(('100+50*10', 600, 16), [75,2,2], variance=True)) # 616
    print(616, make_up_difference(('100+50*10', 600, 16), [75,2,2]))                # 616'''

    '''print('output:', crunch_numbers([9,100,50,25],4,882,10))
    print('output:', crunch_numbers([100,75, 25, 50, 10, 9],4,882,10))
    print('output:', crunch_numbers([100,75, 50, 10, 2, 2],4,616,10))'''

    '''print('output:', crunch_numbers([25,50,3,5,3,7],4, 684,10))
    print('output:', crunch_numbers([25,50,3,5,3,7],5, 684,10))
    print('output:', crunch_numbers([25,50,3,5,3,7],6, 684,10))'''

    '''print('output:', crunch_numbers([25,50,3,5,3],3, 95,1))
    print('output:', crunch_numbers([25,50,3,5,3],4, 95,1))
    print('output:', crunch_numbers([25,50,3,5,3],5, 95,1))'''

    '''print('do_rough_rough_factorization', 684, do_rough_rough_factorization([25,50,3,5,3,7], 684, False))
    print('do_rough_rough_factorization', 681, do_rough_rough_factorization([25,50,3,5,3,7], 681, False))
    print('do_rough_rough_factorization', 679, do_rough_rough_factorization([25,50,3,5,3,7], 679, False))
    print('do_rough_rough_factorization', 675, do_rough_rough_factorization([25,50,3,5,3,7], 675, False))
    print('do_rough_rough_factorization', 674, do_rough_rough_factorization([25,50,3,5,3,7], 674, False))
    print('do_rough_rough_factorization', 673, do_rough_rough_factorization([25,50,3,5,3,7], 673, False))
    print('do_rough_rough_factorization', 672, do_rough_rough_factorization([25,50,3,5,3,7], 672, False))
    print('do_rough_rough_factorization', 671, do_rough_rough_factorization([25,50,3,5,3,7], 671, False))'''
    #print('do_rough_rough_factorization', 810, do_rough_rough_factorization([100, 6, 3, 2, 3, 2], 810, False))

    '''
    print('do_small_factorization', 500, do_small_factorization([100, 75, 10, 9, 7, 5], 500, False))
    print('do_small_factorization', 501, do_small_factorization([100, 75, 10, 9, 7, 5], 501, False))
    print('do_small_factorization', 503, do_small_factorization([100, 75, 10, 9, 7, 5], 503, False))
    print('do_small_factorization', 504, do_small_factorization([100, 75, 10, 9, 7, 5], 504, False))
    print('do_small_factorization', 505, do_small_factorization([100, 75, 10, 9, 7, 5], 505, False))
    print('do_small_factorization', 506, do_small_factorization([100, 75, 10, 9, 7, 5], 506, False))
    print('do_small_factorization', 507, do_small_factorization([100, 75, 10, 9, 7, 5], 507, False))
    print('do_small_factorization', 508, do_small_factorization([100, 75, 10, 9, 7, 5], 508, False))
    print('do_small_factorization', 509, do_small_factorization([100, 75, 10, 9, 7, 5], 509, False))
    print('do_small_factorization', 510, do_small_factorization([100, 75, 10, 9, 7, 5], 510, False))
    print('do_small_factorization', 511, do_small_factorization([100, 75, 10, 9, 7, 5], 511, False))
    print('do_small_factorization', 512, do_small_factorization([100, 75, 10, 9, 7, 5], 512, False))
    print('do_small_factorization', 515, do_small_factorization([100, 75, 10, 9, 7, 5], 515, False))
    print('do_small_factorization', 520, do_small_factorization([100, 75, 10, 9, 7, 5], 520, False))
    print('do_small_factorization', 802, do_small_factorization([100, 7, 1, 8, 2, 8], 802, False))

    print(crunch_numbers([50, 25, 100, 75, 1], 1, 55, 0))
    print(crunch_numbers([50, 25, 100, 75, 1], 2, 55, 0))
    print(crunch_numbers([50, 25, 100, 75, 1], 3, 55, 0))
    print(crunch_numbers([50, 25, 100, 75, 1], 4, 55, 0))
    '''
    '''
    print('do_3_3_split', do_3_3_split([100, 6, 3, 2, 3, 2], 218, False))
    print('do_3_3_split', do_3_3_split([10, 5, 3, 2, 3, 2], 169, False))
    print('do_3_3_split', do_3_3_split([100, 75, 2, 25, 5, 1], 600, False))
    print('do_3_3_split', do_3_3_split([100, 7, 1, 50, 2, 1], 600, False))
    print('do_3_3_split', do_3_3_split([100, 6, 1, 50, 2, 1], 701, False))
    '''
    #print('apply_brackets_4', apply_brackets_4('1+2-3*4'))
    #print('do_4_2_split', do_4_2_split([100, 6, 3, 2, 3, 2], 226, False))
    #print('do_split 4', do_split([100, 6, 3, 2, 3, 2], 4, 226, False))
    #print('do_4_2_split', do_4_2_split([100, 6, 1, 50, 2, 1], 708, False))
    #print('do_split 4', do_split([100, 6, 1, 50, 2, 1], 4, 708, False))
    #print('do_3_3_split', do_3_3_split([100, 6, 1, 50, 2, 1], 708, False))
    print('do_split 3', do_split([100, 6, 1, 50, 2, 1], 3, 708, False))
    print('do_split 3', do_split([100, 1, 6, 10, 8, 9], 3, 381, False))
    print('do_split 3', do_split([75, 50, 25, 5, 8, 8], 3, 852, False))
    print('do_split 4', do_split([75, 50, 25, 5, 8, 8], 4, 852, False))

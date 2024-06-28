#!/usr/bin/python3
import random
import re
import time
import warnings
import json
from itertools import combinations
from itertools import permutations
from itertools import product
from numberutils import factorize_by_trial_division

LARGE_NUMBERS = [100, 75, 50, 25]
checkpoint = False

def complement(a:list, b:tuple):
    c = a.copy()
    for x in b:
        c.remove(x)
    return tuple(c)

def rebuild_expression(expr: str, tkns: list[tuple], debug:bool=False) -> str:
    tokens = tkns.copy()
    tokens.reverse()
    expression = expr
    try:
        result = eval(expression)
    except:
        return expression
    
    for t in tokens:
        pattn = re.compile(t[0])
        offs = 0
        while True:
            r = pattn.search(expression, offs)
            if not r:
                if debug:
                    print('rebuild_expression', r, tokens, t, expression, result, offs, expr)
                break
            offs+= r.span()[1]
            brk = r.span()[0]
            expression_sav = expression
            expression = expression[:brk] + expression[brk:].replace(t[0], '(' + t[1] + ')', 1)
            try:
                r = eval(expression)
                if int(r) == result:
                    break
                else:
                    expression = expression_sav
            except:
                expression = expression_sav
                continue
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
                    expression = expression.replace(g, s, 1)
                    tokens.append((s, g))
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
    if not r:
        return res
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

def evaluate_switching_precedence(expression: str, target: int, variance: int, debug:bool=False) -> tuple:
    ''' 
    Evaluate switching precedence to (+, -, *, /) by doing addition and subtraction first
    '''
    tokens = []
    res = ()
    if debug:
        print('evaluate_switching_precedence', expression)
    while True:
        r = re.search(r'\d+[\+\-]\d+',expression)
        if r:
            g = r.group()
            s = str(eval(g))
            tokens.append((s, g))
            expression = expression.replace(g, s, 1)
            if debug:
                print('evaluate_switching_precedence', tokens, expression)
            try:
                r = eval(expression)
                diff = target - r
                int_r = int(r)
                if diff == int(diff) and abs(diff) <= variance:
                    expression2 = rebuild_expression(expression, tokens, debug=debug)    # explain workings
                    if res:
                        if abs(diff) < abs(res[2]): 
                            res = (expression2, int_r, int(diff))
                    else:
                        res = (expression2, int_r, int(diff))
                    if diff == 0:
                        return res
            except:
                continue
        else:
            break

    return res

def make_up_difference(target:int, soln:tuple, nos:list[int], var:bool=False) -> tuple:

    #Try to make a small difference value from a small subset of numbers
    
    len_nos = len(nos)
    expression = soln[0]
    diff = soln[2]
    if len_nos > 4:
        return ()
    else:
        ret = ()
        res = (crunch_numbers(nos, x+1, abs(diff), 0) for x in range(len_nos-1)) #restrict perms to save time
        for r in res:
            if r:
                if diff < 0:
                    ret = ('('+expression+')-('+r[0]+')', target, 0)
                else:
                    ret = ('('+expression+')+('+r[0]+')', target, 0)
                break
        return ret

'''def make_up_difference(target:int, soln:tuple, nos:list[int], variance:bool=False) -> tuple:
    
    #Try to make a small difference value from a small subset of numbers
    
    len_nos = len(nos)
    expression = soln[0]
    result = soln[1]
    diff = soln[2]
    if variance:
        tolerance = abs(diff)-1
    else:
        tolerance = 0
    if len_nos > 4:
        return ()
    else:
        ret = ()
        res = (crunch_numbers(nos, x+1, abs(diff), tolerance) for x in range(len_nos-1)) #restrict perms to save time
        bestr = ('', 0, 999)
        for r in res:
            if r and abs(r[2]) < bestr[2]:
                bestr = r
        if bestr and bestr[0]:
            if diff < 0:
                t = result - bestr[1]
                ret = ('('+expression+')-('+bestr[0]+')', t, -1*bestr[2])
            else:
                t = result + bestr[1]
                ret = ('('+expression+')+('+bestr[0]+')', t, bestr[2])
        return ret'''

def crunch_numbers(nos:list[int], permsize:int, target:int, variance:int, debug:bool=False) -> tuple:
    '''
    Brute force our way through mathematical expressions
    made from all permutations of size <permsize> of numbers 
    and the operators (+, -, *, /)
    '''
    OPERATIONS = ("+", "-", "*", "/")
    res = ()
    j = 1
    opslist = []
    while j < permsize:
        opslist.append(OPERATIONS)
        j+= 1
    operators = tuple(product(*opslist))
    for n in permutations(nos, permsize):
        for o in operators:
            expression = ""
            j = 0
            olim = len(o)
            while j < len(n):   # Make the arithmetic expression
                expression+= str(n[j])
                if j < olim:
                    expression+= o[j]
                j+= 1

            nos2 = strip_numbers(expression, nos)   # The numbers that are left

            # Evaluate expression using conventional operator precedence (*, /, +, -)
            res2 = evaluate_conventional(expression, target, variance)
            if res2 and res2[2] == 0:
                return res2
            if res2:
                if not res:
                    res = res2
                elif abs(res2[2]) < abs(res[2]):
                    res = res2
            # Try to make the difference up
            if res2 and res2[2] != 0:
                res2 = make_up_difference(target, res2, nos2, True)
                if res2:
                    return res2

            # If that didn't work evaluate expression in order of appearance
            res2 = evaluate_in_order(expression, target, variance)
            if res2 and res2[2] == 0:
                return res2
            if res2:
                if not res:
                    res = res2
                elif abs(res2[2]) < abs(res[2]):
                    res = res2
            # Try to make the difference up
            if res2 and res2[2] != 0:
                res2 = make_up_difference(target, res2, nos2, True)
                if res2:
                    return res2

            # If that didn't work didn't try parenthesis
            res2 = evaluate_with_parenthesis(expression, target, variance)
            if res2 and debug and abs(res2[2])<2:
                print("evaluate_with_parenthesis", res2)
            if res2 and res2[2] == 0:
                return res2
            if res2:
                if not res:
                    res = res2
                elif abs(res2[2]) < abs(res[2]):
                    res = res2
            # Try to make the difference up
            if res2 and res2[2] != 0:
                res2 = make_up_difference(target, res2, nos2, True)
                if res2:
                    return res2

            # If that didn't work switch precedence to (+, -, *, /) by evaluating 
            # addition and subtraction first
            res2 = evaluate_switching_precedence(expression, target, variance, debug=debug)
            if res2 and debug and abs(res2[2])<2:
                print("evaluate_switching_precedence", res2)
            if res2 and res2[2] == 0:
                res = res2
                return res
            if res2:
                if not res:
                    res = res2
                elif abs(res2[2]) < abs(res[2]):
                    res = res2
            # Try to make the difference up
            if res2 and res2[2] != 0:
                res2 = make_up_difference(target, res2, nos2, True)
                if res2:
                    return res2
            
    return res

def do_numbers(nos:list[int], target:int, variance:int, silent:bool=False) -> tuple:
    ''' 
    Find a target number within variance by applying the mathematical operators
    supplied (+, -, * or /) on a list of numbers provided (note that each number 
    can only be used once).
    '''
    if target in nos:
        return (str(int(target)), target, 0)
    res = ()
    noslen = len(nos)
    i = 2
    global checkpoint
    while i <= noslen:
        # Timeout, return best answer
        if checkpoint:
            #if silent:
            #    return(res)
            #else:
            #    print("Timeout warning!")
            #if res:
            #    checkpoint = False
            #    newnos = strip_numbers(res[0], nos)
            #    newres = do_numbers(newnos, abs(res[2]), 0, silent=True)
            #    checkpoint = True
            #    if newres:
            #        if res[1] > 0:
            #            return (res[0]+"+"+newres[0], target, 0)
            #        else:
            #            return (res[0]+"-"+newres[0], target, 0)
            print("Best:", format_solution(res))
            ex = input("Stop(N)? ") or 'N'
            if ex.upper() != 'N':
                return res
        elif not silent and res and i > 2:
            print("Best:", format_solution(res))

        res2 = crunch_numbers(nos, i, target, variance)
        ok = check_solution(res2)
        if ok:
            if res2[2] == 0:
                res = res2
                break
            if not res:
                res = res2
            elif abs(res2[2]) < abs(res[2]):
                res = res2
        i+= 1
    
    return res

def strip_numbers(expr:str, nos:list[int]) -> list[int]:
    '''
    Strip numbers in a mathematical expression from a list
    provided and return the unused numbers
    '''
    numbers = nos.copy()
    l = re.findall(r'\d+', expr)
    for n in l:
        int_n = int(n)
        if int_n in numbers:
            numbers.remove(int_n)
    return numbers    

def do_prime_factorization(numbers:list[int], target:int) -> tuple:
    res = ()
    factors = factorize_by_trial_division(target)
    if not factors: # target is prime
        return ()
    used = []
    for f in factors:
        if f in used:
            continue
        nos = numbers.copy()
        r1 = do_numbers(nos, f, 0, silent=True)
        if r1:
            nos = strip_numbers(r1[0], nos)     # remove used numbers from number list
            multiplier = target // f            # factor * multiplier = target
            r2 = do_numbers(nos, multiplier, 0, silent=True)
            if r2:
                res = ('(' + r2[0] + ')*(' + r1[0] + ')', target, 0)
            used.append(f)
            used.append(multiplier)
        if res:
            break

    return res

def do_rough_factorization(numbers:list[int], target:int, debug:bool=False) -> tuple:
    ''' Roughly factorize using the large numbers '''
    best = ()
    for large in LARGE_NUMBERS:
        nos = numbers.copy()
        if not large in nos:
            continue
        nos.remove(large)
        q1 = target // large
        q2 = q1 + 1
        for q in (q1, q2):              # each quotient
            p = q * large               # product      
            r = target - p              # remainder
            if debug:
                print(large, p, q, r)
            # We need to make quotient and remainder from numbers list
            qres = (crunch_numbers(nos, x+1, q, 0) for x in range(4))
            for resq in qres:
                if debug:
                    print('resq',resq)
                if not resq:
                    continue
                if r == 0:  # no remainder
                    expr=str(large)+'*('+str(resq[0])+')'
                    best = (expr, int(eval(expr)), 0)
                    return best
                newlist = strip_numbers(resq[0], nos)
                if debug:
                    print('newlist', newlist)
                if newlist:
                    rres = (crunch_numbers(newlist, x+1, abs(r), 0) for x in range(len(newlist)))
                    for resr in rres:
                        if debug:
                            print('resr',resr)
                        if not resr:
                            continue
                        v = large*resq[1]
                        expr=str(large)+'*('+str(resq[0])+')'
                        if r < 0:
                            v-=resr[1]
                            expr=expr+'-('+str(resr[0])+')'
                        else:
                            v+=resr[1]
                            expr=expr+'+('+str(resr[0])+')'
                        if not best:
                            best = (expr, v, target-v)
                            return best
    return best

def do_rough_rough_factorization(numbers:list[int], target:int, debug:bool=False) -> tuple:
    ''' Very roughly factorize using the large numbers '''
    best = ()
    for large in LARGE_NUMBERS:
        nos = numbers.copy()
        q1 = target // large
        q2 = q1 + 1
        for q in (q1, q2):              # each quotient
            d = target // q             # get denominator
            p = q * d                   # product
            r = target - p              # remainder
            if debug:
                print('do_rough_rough_factorization', target, p, q, d, r)
            # We need to make quotient, denominator and remainder from numbers list
            qres = (crunch_numbers(nos, x+1, q, 0) for x in range(3))
            for resq in qres:
                if not resq:
                    continue
                if debug:
                    print('resq',resq)
                newlist = strip_numbers(resq[0], nos)
                if debug:
                    print('newlist', newlist)
                if newlist:
                    for dd in (d-1, d, d+1):
                        dres = (crunch_numbers(newlist, x+1, dd, 0) for x in range(min(3,len(newlist))))
                        for resd in dres:
                            if not resd:
                                continue
                            if debug:
                                print('resd',resd)
                            p = q * resd[1]
                            r = target - p
                            if r == 0:
                                bestexpr = '('+resd[0]+')*('+resq[0]+')'
                                p = int(eval(bestexpr))
                                best = (bestexpr, p, target-p)
                                if debug:
                                    print('1. best updated', best)
                                return best
                            else:
                                newnewlist = strip_numbers(resd[0], newlist)
                                if debug:
                                    print('newnewlist', newnewlist)
                                if newnewlist:
                                    rres = (crunch_numbers(newnewlist, x+1, abs(r), r-1) for x in range(len(newnewlist)))
                                    bestr = ('', 0, 999)
                                    for resr in rres:
                                        if not resr:
                                            continue
                                        if debug:
                                            print('resr',resr)
                                        if abs(resr[2]) < abs(bestr[2]):
                                            bestr = resr
                                    if not best or abs(bestr[2])<abs(best[2]):
                                        bestexpr = '('+resd[0]+')*('+resq[0]+')'
                                        if bestr[0]:
                                            if r > 0:
                                                bestexpr+= '+('+bestr[0]+')'
                                            else:
                                                bestexpr+= '-('+bestr[0]+')'
                                        if debug:
                                            print(best, bestr)
                                        p = int(eval(bestexpr))
                                        best = (bestexpr, p, target-p)
                                        if debug:
                                            print('2. best updated', best)
                                    if best[2]==0:
                                        return best
                                else:
                                    bestexpr = '('+resd[0]+')*('+resq[0]+')'
                                    p = int(eval(bestexpr))
                                    r = target - p
                                    if not best or abs(r) < abs(best[2]):
                                        best = (bestexpr, p, r)
                                        if debug:
                                            print('3. best updated', best)

    return best

def do_small_factorization(numbers:list[int], target:int, debug:bool=False) -> tuple:
    ''' Roughly factorize using the small numbers '''
    best = ()
    for small in numbers:
        if small > 10:
            continue
        nos = numbers.copy()
        nos.remove(small)
        q0 = target // small
        if q0 < 6:
            q0 = 6
        for q in range(q0-5, q0+6):     # range of quotients
            p = q * small               # product      
            r = target - p              # remainder
            if debug:
                print(small, nos, p, q, r)
            # We need to make quotient and remainder from numbers list
            if q in nos and r == 0:
                best = (str(small)+'*'+str(q), target, 0)
                return best
            qres = (crunch_numbers(nos, x+1, q, 0) for x in range(4))
            for resq in qres:
                if debug:
                    print('resq',resq)
                if not resq:
                    continue
                if r == 0:  # no remainder
                    expr=str(small)+'*('+str(resq[0])+')'
                    best = (expr, int(eval(expr)), 0)
                    return best
                newlist = strip_numbers(resq[0], nos)
                if debug:
                    print('newlist', newlist)
                if newlist:
                    rres = (crunch_numbers(newlist, x+1, abs(r), 0) for x in range(len(newlist)))
                    for resr in rres:
                        if debug:
                            print('resr',resr)
                        if not resr:
                            continue
                        v = small*resq[1]
                        expr=str(small)+'*('+str(resq[0])+')'
                        if r < 0:
                            v-=resr[1]
                            expr=expr+'-('+str(resr[0])+')'
                        else:
                            v+=resr[1]
                            expr=expr+'+('+str(resr[0])+')'
                        if not best:
                            best = (expr, v, target-v)
                            return best
    return best

def apply_brackets(expression:str):
    nos = re.split(r'[\+\-\*\/]', expression)
    len_nos = len(nos)
    match len_nos:
        case 3:
            return apply_brackets_3(expression)
        case 4:
            return apply_brackets_4(expression)
        case _:
            return ''

def apply_brackets_3(expression:str):
    expressions = []
    nos = re.split(r'[\+\-\*\/]', expression)
    if len(nos) != 3:
        return ''
    ops = re.split(r'\d+', expression)
    ops = [x for x in ops if x]
    e = '('+nos[0]+ops[0]+nos[1]+')'+ops[1]+nos[2]
    expressions.append(e)
    e = nos[0]+ops[0]+'('+nos[1]+ops[1]+nos[2]+')'
    expressions.append(e)
    return expressions

def apply_brackets_4(expression:str):
    expressions = []
    nos = re.split(r'[\+\-\*\/]', expression)
    if len(nos) != 4:
        return ''
    ops = re.split(r'\d+', expression)
    ops = [x for x in ops if x]
    e = '('+nos[0]+ops[0]+nos[1]+')'+ops[1]+'('+nos[2]+ops[2]+nos[3]+')'
    expressions.append(e)
    e = '('+nos[0]+ops[0]+nos[1]+')'+ops[1]+nos[2]+ops[2]+nos[3]
    expressions.append(e)
    e = nos[0]+ops[0]+'('+nos[1]+ops[1]+nos[2]+')'+ops[2]+nos[3]
    expressions.append(e)
    e = nos[0]+ops[0]+nos[1]+ops[1]+'('+nos[2]+ops[2]+nos[3]+')'
    expressions.append(e)
    e = '('+nos[0]+ops[0]+nos[1]+ops[1]+nos[2]+')'+ops[2]+nos[3]
    expressions.append(e)
    e = nos[0]+ops[0]+'('+nos[1]+ops[1]+nos[2]+ops[2]+nos[3]+')'
    expressions.append(e)
    return expressions

def do_split(numbers:list[int], size:int, target:int, debug:bool=False) -> tuple:
    ''' 
    Split numbers list into 2 groups (larger group indicated by size argument)
    and try to make the target
    '''
    OPERATIONS = ("+", "-", "*", "/")
    j = 1
    opslist = []
    while j < size:
        opslist.append(OPERATIONS)
        j+= 1
    operators = tuple(product(*opslist))
    for c in combinations(numbers, size):
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

def check_solution(solutions:tuple) -> bool:
    if not solutions:
        return False
    quotients = re.findall(r'\d+/\d+', solutions[0])
    for q in quotients:
        eval_q = eval(q)
        if eval_q != int(eval_q):
            return False
    return True

def format_solution(solutions:tuple) -> str:
    if solutions:
        return solutions[0]+' | '+str(solutions[1])+' | '+str(solutions[2])
    else:
        return "No solution"

def numbers_main(number_list:list[int], target:int, silent:bool=False, autofile:bool=False) -> tuple:
    starttime = time.time()
    if autofile:
        statsfile_name = 'stats-'+autofile+'.json'
    else:
        statsfile_name = "stats.json"
    global checkpoint
    checkpoint = False
    solutions = None
    if not solutions:
        attempting = "do_split 3,3"
        if not silent:
            print(attempting)
        checkpointtime = time.time()
        solutions = do_split(number_list, 3, target, False)
    if not solutions:
        attempting = "do_small_factorization"
        if not silent:
            print(attempting)
        checkpointtime = time.time()
        solutions = do_small_factorization(number_list, target)
    if not solutions:
        attempting = "do_prime_factorization"
        if not silent:
            print(attempting)
        checkpointtime = time.time()
        solutions = do_prime_factorization(number_list, target)
    if not solutions:
        attempting = "do_rough_factorization"
        if not silent:
            print(attempting)
        checkpointtime = time.time()
        solutions = do_rough_factorization(number_list, target)
    if not solutions:
        attempting = "do_rough_rough_factorization"
        if not silent:
            print(attempting)
        checkpointtime = time.time()
        solutions = do_rough_rough_factorization(number_list, target)
    if not solutions or solutions[2] != 0:
        attempting = "do_numbers_(brute_force)"
        if not silent:
            checkpoint = True
            print(attempting)
        checkpointtime = time.time()
        solutions = do_numbers(number_list, target, 100, silent)
    currenttime = time.time()
    time_taken = int(currenttime-starttime)+1
    step_time = int(currenttime-checkpointtime)+1
    if solutions and solutions[2] == 0:
        # Log how solution was achieved to provide stats to help improve
        statsfile = None
        try:
            statsfile = open(statsfile_name,'r')
            statsobj = json.loads(statsfile.read())
        except:
            statsobj = {}
        if attempting in statsobj:
            statsobj[attempting][0]+= 1
            statsobj[attempting][1]+= step_time
        else:
            statsobj[attempting] = [1, step_time]
        if statsfile:
            statsfile.close()
        statsfile = open(statsfile_name,'w')
        statsfile.write(json.dumps(statsobj))
        statsfile.close()
    return (time_taken, solutions)

def get_some_numbers() -> tuple:
    number_list = []
    large_numbers = LARGE_NUMBERS.copy()
    lrg = random.randint(0, 4)
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
    return (number_list, numbers)

if __name__ == '__main__':
    warnings.filterwarnings('error')
    while True:
        numbers = input("Enter your numbers: ").strip().lower()
        if numbers == "quit" or numbers == "exit":
            break
        if not numbers:
            (number_list, numbers) = get_some_numbers()
        else:
            try:
                number_list = [int(x) for x in numbers.split(" ")]
            except:
                continue
        if len(number_list) != 6:
            continue
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
        print("Numbers:", numbers)
        print("Target:", target)
        (time_taken, solutions) = numbers_main(number_list, target)
        print("Execution:", time_taken, "seconds")
        print("Solution:", format_solution(solutions))

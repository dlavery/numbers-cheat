#!/usr/bin/python3
PRIMES_1 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]         # prime numbers < sqrt(999)
PRIMES_2 = [37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
            79, 83, 89, 97, 101, 103, 107, 109, 113, 127,
            131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
            181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
            239, 241, 251, 257, 263, 269, 271, 277, 281, 283,
            293, 307, 311, 313, 317, 331, 337, 347, 349, 353,
            359, 367, 373, 379, 383, 389, 397, 401, 409, 419,
            421, 431, 433, 439, 443, 449, 457, 461, 463, 467,
            479, 487, 491, 499]                             # sqrt(999) <= prime numbers < 999 / 2

def factorize_by_trial_division(n: int) -> list[int]:
    """
    Return a list of the prime factors for a natural number.
    An empty list indicates that the number itself is prime
    """
    a = []                              # Prepare an empty list.
    primes_iter = iter(PRIMES_1)
    f = next(primes_iter)               # The first possible factor.    
    while n > 1:                        # While n still has remaining factors...
        if n % f == 0:                  # The remainder of n divided by f might be zero.        
            a.append(f)                 # If so, it divides n. Add f to the list.
            n //= f                     # Divide that factor out of n.
            if n in PRIMES_2:           # If other factor is prime, add to list and stop
                a.append(n)
                break
        else:
            try:                        # But if f is not a factor of n,
                f = next(primes_iter)   # Set f to the next prime and try again.
            except StopIteration:
                break
    return a                            # Prime factors may be repeated: 12 factors to 2,2,3.

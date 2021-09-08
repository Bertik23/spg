import time


def prime(num):
    start = time.time()
    primes = []
    if num >= 3:
        primes.append(2)
    for n in range(3, num, 2):
        p = True
        for prime in primes:
            # print(prime)
            if n % prime == 0:
                p = False
                break
        if p:
            primes.append(n)
    print(time.time() - start)
    return primes


ps = prime(1000000)

print(len(ps))

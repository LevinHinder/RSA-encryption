import math
import os


def are_coprime(a, n):
    return math.gcd(a, n) == 1


def miller_rabin_test(a, n):
    s = 0
    while (n - 1) % (2 ** (s + 1)) == 0:
        s += 1

    d = (n - 1) // (2 ** s)

    if mod_exponentiation(a, d, n) == 1:
        return True
    for r in range(s):
        if mod_exponentiation(a, (2 ** r) * d, n) == n - 1:
            return True
    return False


def random(length):
    random_data = os.urandom(length)
    number = ""

    for num in list(random_data):
        number += str(num)[-1]

    return int(number)


def generate_prime(length, iterations=4, length_a=10):
    prime = random(length)
    i = 0

    while i <= iterations:
        a = random(length_a)
        while not are_coprime(a, prime):
            a = random(length_a)
        if not miller_rabin_test(a, prime):
            prime = random(length)
            i = 0
        else:
            i += 1

    return prime


def mod_exponentiation(a, b, n):
    b_bin = bin(b)[2:]
    result = 1

    a = (a ** 1) % n
    if b_bin[-1] == "1":
        result *= a
        result %= n

    for i in range(1, len(b_bin)):
        a = (a ** 2) % n

        if b_bin[-i - 1] == "1":
            result *= a
            result %= n

    return result


def extended_euclidean(a, b):
    A = a
    s2, t2, s1, t1 = 1, 0, 0, 1

    while b > 0:
        q = a // b
        r, s, t = (a - b * q), (s2 - q * s1), (t2 - q * t1)
        a, b, s2, t2, s1, t1 = b, r, s1, t1, s, t
    t = t2

    if t >= 0:
        return t
    else:
        return A + t


def encode(m, e, n):
    if m < 0 or m >= n:
        return None

    c = mod_exponentiation(m, e, n)
    return c


def decode(c, d, n):
    if c < 0 or c >= n:
        return None

    m = mod_exponentiation(c, d, n)
    return m


p = generate_prime(100)
q = generate_prime(100)

n = p * q
phi = (p - 1) * (q - 1)

e = random(50)
while not are_coprime(e, phi):
    e = random(50)

d = extended_euclidean(phi, e)

message = 651651313165432132163514631321365161316463210321651303206513130356

c = encode(message, e, n)
m = decode(c, d, n)

print(m)

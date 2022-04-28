from prime_generator import  get_big_prime

def generate_keys():
    p = get_big_prime()
    q = get_big_prime()

    n = p * q
    euler = (p - 1) * (q - 1)

    e = 2
    while gcd(e, euler) != 1:
        e += 1

    d = extended_euclid(n, e)[2] % n

    return (n, e), (n, d)


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def extended_euclid(a, b):
    if b == 0:
        return a, 1, 0
    d, x, y = extended_euclid(b, a % b)
    return d, y, x - (a // b) * y


def encrypt(msg: int, e, n):
    return (msg ** e) % n


def decrypt(encrypted: int, e, n):
    pass
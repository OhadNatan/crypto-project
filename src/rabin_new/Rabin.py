# Rabin.py
import prime

# encryption function
# plaintext is a 224-bit number
def encryption(plaintext, n):
    # c = m^2 mod n
    plaintext = padding(plaintext)
    return plaintext ** 2 % n


# padding 16 bits to the end of a number
def padding(plaintext):
    binary_str = bin(plaintext)     # convert to a bit string
    output = binary_str + binary_str[-16:]      # pad the last 16 bits to the end
    return int(output, 2)       # convert back to integer


# encryption function
def decryption(a, p, q, m):
    n = p * q
    r, s = 0, 0
    # find sqrt
    # for p
    if p % 4 == 3:
        r = prime.sqrt_p_3_mod_4(a, p)
    elif p % 8 == 5:
        r = prime.sqrt_p_5_mod_8(a, p)
    # for q
    if q % 4 == 3:
        s = prime.sqrt_p_3_mod_4(a, q)
    elif q % 8 == 5:
        s = prime.sqrt_p_5_mod_8(a, q)

    _, x, y = prime.egcd(p, q)
    m1 = (r * y * q + s * x * p) % n
    m2 = (r * y * q - s * x * p) % n
    lst = [m1, n - m1, m2, n - m2]

    return verify(lst, m)


def verify(lst, m):
    for m_i in lst:
        string = bin(m_i)
        string = string[:-16]
        plaintext = int(string, 2)
        if plaintext == m:
            return True

    return False


def generate_keys_for_rabin():
    p = prime.generate_a_prime_number()
    q = prime.generate_a_prime_number()
    while q == p:
        q = prime.generate_a_prime_number()

    return p, q, q*p

if __name__ == "__main__":
    print(generate_keys_for_rabin())
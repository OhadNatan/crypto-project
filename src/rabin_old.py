import hashlib, sys
import random


def gcd(a, b):
    if b > a:
        a, b = b, a
    while b > 0:
        a, b = b, a % b
    return a


def nextPrime(p):
    while p % 4 != 3:
        p = p + 1
    return nextPrime_3(p)


def nextPrime_3(p):
    m_ = 3 * 5 * 7 * 11 * 13 * 17 * 19 * 23 * 29
    while gcd(p, m_) != 1:
        p = p + 4
    if (pow(2, p - 1, p) != 1):
        return nextPrime_3(p + 4)
    if (pow(3, p - 1, p) != 1):
        return nextPrime_3(p + 4)
    if (pow(5, p - 1, p) != 1):
        return nextPrime_3(p + 4)
    if (pow(17, p - 1, p) != 1):
        return nextPrime_3(p + 4)
    return p


# x: bytes
# return: int
def h(x):
    hx = hashlib.sha256(x).digest()
    idx = len(hx) // 2
    hl = hashlib.sha256(hx[:idx]).digest()
    hr = hashlib.sha256(hx[idx:]).digest()
    return int.from_bytes(hl + hr, 'little')


# m: bytes
def root(m, p, q):
    i = 0
    nrabin = p*q
    while True:
        x = h(m) % nrabin
        sig = pow(p, q - 2, q) * p * pow(x, (q + 1) // 4, q)
        sig = (pow(q, p - 2, p) * q * pow(x, (p + 1) // 4, p) + sig) % (nrabin)
        if (sig * sig) % nrabin == x and i != 0:
            break
        m = m + bytes.fromhex("00")
        i = i + 1
    print("paddingnum: " + str(i))
    return sig, i


def writeNumber(number, fnam):
    with open(fnam + '.txt', 'w') as f:
        f.write('%d' % number)


def hF(m, paddingnum, nrabin):
    return h(m + bytes.fromhex("00") * paddingnum) % nrabin


def sF(hexmsg, p, q):
    return root(bytes.fromhex(hexmsg), p, q)


def vF(hexmsg, paddingnum, s, nrabin):
    return hF(bytes.fromhex(hexmsg), paddingnum, nrabin) == (s * s) % nrabin


def generate_keys_for_rabin():
    arg = '{}{}'.format((random.randint(a=0, b=9)), random.randint(a=0, b=9))
    p = nextPrime(h(bytes.fromhex(arg)) % (2 ** 501 + 1))
    q = nextPrime(h(bytes.fromhex(arg + '00')) % (2 ** 501 + 1))
    return p, q, p * q


def sing_msg(msg, p, q):
    sig, padding_num = sF(msg, p, q)
    return hex(sig), padding_num


def verify(to_ver, sig, padding_num, nrabin):
    print("result of verification: " + str(vF(to_ver, int(padding_num), int(sig, 16), nrabin)))


def main(choice=None, msg=None, p=None, q=None, n=None, padding_num=None, sig=None):

    if choice == "V" and msg and sig and padding_num:
        verify(msg, sig, padding_num, n)

    if choice == "S" and p and q and msg:
        return sing_msg(msg, p, q)

    if choice == "G":
        return generate_keys_for_rabin()


msg_to_sig = '00112233445566778899aabbccddeeff'
p, q, n = main('G')

sig, pad_num = main('S', msg=msg_to_sig, p=p, q=q)

main('V', sig=sig, msg=msg_to_sig, padding_num=pad_num, n=n)

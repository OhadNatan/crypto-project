import hashlib, sys

nrabin = 0x1541942cc552a95c4832350ce99c2970f5b3ce9237a09c70c0e867d28039c05209b601105d3b3634cdaee4931809bc0c41d6165a0df16829a3a31202f56003239dd2c6e12297e94ef03e6aa61a147ea2b51c476dc45f5a2406b66d1ece2755c1f3d4144c0a42acc99b599d0643654a4cac392efbcf3db84d4233834afd1


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
    while True:
        x = h(m) % nrabin
        sig = pow(p, q - 2, q) * p * pow(x, (q + 1) // 4, q)
        sig = (pow(q, p - 2, p) * q * pow(x, (p + 1) // 4, p) + sig) % (nrabin)
        if (sig * sig) % nrabin == x:
            break
        m = m + bytes.fromhex("00")
        i = i + 1
    print("paddingnum: " + str(i))
    return sig


def writeNumber(number, fnam):
    with open(fnam + '.txt', 'w') as f:
        f.write('%d' % number)


def readNumber(fnam):
    with open(fnam + '.txt', 'r') as f:
        return int(f.read())


def hF(m, paddingnum):
    return h(m + bytes.fromhex("00") * paddingnum) % nrabin


def sF(hexmsg):
    p = readNumber("p")
    q = readNumber("q")
    return root(bytes.fromhex(hexmsg), p, q)


def vF(hexmsg, paddingnum, s):
    return hF(bytes.fromhex(hexmsg), paddingnum) == (s * s) % nrabin

if __name__ == '__main__':
    choice = 'S'

    if choice == "V":
        to_ver = '00112233445566778899aabbccddeeff'
        paddingnum = '5'
        digital = '0x10072ba7f1494016ad6193ea1862ffd2e570fbe1a765ec68641853db28ba44734a011f282b79a4321dee7bd9585f02a5cf8162f7ded88a98320577aec11cb55951779657df3dd65599813a4ffb93608a3b36b345cfe71dc7ac38e69402c2fc26edc988b68ba5865b126cf8fd2be2afd239ea05dc711771f658a07e69927'
        print("result of verification: " + str(vF(to_ver, int(paddingnum), int(digital, 16))))

    if choice == "S":
        msg = '00112233445566778899aabbccddeeff'
        print((" digital signature:\n " + hex(sF(msg))))

    if choice == "G":
        arg = '01'
        print(" generate primes ... ")
        p = nextPrime(h(bytes.fromhex(arg)) % (2 ** 501 + 1))
        q = nextPrime(h(bytes.fromhex(arg + '00')) % (2 ** 501 + 1))
        writeNumber(p, 'p')
        writeNumber(q, 'q')
        print("nrabin = ", hex(p * q))
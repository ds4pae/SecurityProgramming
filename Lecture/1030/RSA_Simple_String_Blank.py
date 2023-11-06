import random

def gcd(a, b):
    while (b != ????):
        temp = a % b
        a = b
        b = ????
    return abs(a)


def isCoPrime(a, b):
    if gcd(a, b) == ????:
        return ????
    else:
        return False


def modinv(a, n):
    temp = n
    b, c = 1, 0
    while n:
        q, r = divmod(a, n)
        a, n, b, c = n, r, c, ????
    # at this point a is the gcd of the original inputs
    if a == 1:
        return (temp + b) % temp
    raise ValueError("Not invertible")


def getCompleteResidue(m):
    return list(range(0,m))


def getReducedResidue(m):
    reducedResidueList = []
    for x in range(1,m):
        if gcd(x, m) == 1:
            reducedResidueList.append(????)
    return reducedResidueList


def eularPhi(m):
    return len(????????(m))


def tot_list(n):
    phi = []
    x = 1
    while x < n:
        if  ????? == 1:
            phi += [x]
        x += 1
    return phi


def tot_phi(n):
    return len(?????(n))


def isPrime(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return ??????
    return True


def primesInRange(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = ?????

        if isPrime:
            prime_list.append(n)
    return prime_list


def findGenerators(n):
    s = set(range(1, n))
    results = []
    for a in s:
        g = set()
        for x in s:
            g.add((a**x) % n)
        if g == s:
            results.append(a)
    return results


def genRSAKeys(p, q):
    if isPrime(p) & isPrime(q):
        n = p*q
        e = random.choice([x for x in range(1, (p-1)*(q-1)) if isCoPrime(x, (p-1)*(q-1))])
        d = ??????(e, (p-1)*(q-1))
        publicKey = (n, e)
        privateKey = (n, d)
        return publicKey, privateKey
    else:
        print("P and Q : Select Prime Numbers!!!")
        return False


def RSAEncryptSimpleString(msg, publicKey):
    output = []
    n, e = publicKey
    for val in msg:
        output.append(pow(ord(val), ????, n))
    return output


def RSADecryptSimpleString(ciphertext, privateKey):
    output = []
    n, d = privateKey
    for val in ciphertext:
        output.append(chr(pow(val, ????, n)))
    return "".join(output)


def main():
    x = pow(2,11)-100
    y = pow(2,11)
    primeList = primesInRange(x, y)
    p = primeList[-1]
    q = primeList[-2]
    print("primeNumber p: ", p)
    print("primeNumber q: ", q)
    bobPublicKey, bobPrivateKey = genRSAKeys(p, q)
    print("bob's Public Key (n, e): ", bobPublicKey)
    print("bob's Private Key (n, d): ", bobPrivateKey)

    ### RSAEncrypt
    msg = "World !! World"
    print("message: ", msg)
    ciphertext = RSAEncryptSimpleString(msg, bobPublicKey)
    print("ciphertext: ", ciphertext)

    ### RSADecrypt
    decrypt = RSADecryptSimpleString(ciphertext, bobPrivateKey)
    print("plaintext: ", decrypt)

if __name__ =="__main__":
    main()

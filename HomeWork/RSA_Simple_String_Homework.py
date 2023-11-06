import random

from sympy import factorint


def gcd(a, b):      #최대공약수
    while (b != 0):
        temp = a % b
        a = b
        b = temp
    return abs(a)   #abs() = 절대값으로 바꿔줌


def isCoPrime(a, b):    #coPrime = 서로소
    if gcd(a, b) == 1:
        return True
    else:
        return False


def modinv(a, n):
    temp = n
    b, c = 1, 0
    while n:
        q, r = divmod(a, n)
        a, n, b, c = n, r, c, b-q*c
    # at this point a is the gcd of the original inputs
    if a == 1:
        return (temp + b) % temp
    raise ValueError("Not invertible")


def getCompleteResidue(m):  #완전잉여계
    return list(range(0,m))


def getReducedResidue(m):   #기약잉여계
    reducedResidueList = []
    for x in range(1,m):
        if gcd(x, m) == 1:
            reducedResidueList.append(x)
    return reducedResidueList


def eularPhi(m):
    return len(getReducedResidue(m))


def tot_list(n):
    phi = []
    x = 1
    while x < n:
        if gcd(x,n) == 1:
            phi += [x]
        x += 1
    return phi


def tot_phi(n):
    return len(tot_list(n))


def isPrime(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def primesInRange(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False

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
        n = 16695347
        e = 3789479
        d = modinv(e, (p-1)*(q-1))

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
        output.append(pow(ord(val), e, n))
    return output


def RSADecryptSimpleString(ciphertext, privateKey):
    output = []
    n, d = privateKey
    for val in ciphertext:
        output.append(chr(pow(val, d, n)))
    return "".join(output)

def findGenerators(n):
    s = set( num for num in range (1, n) if gcd (num,n) == 1)
    results = []
    for a in s:
        g = set()
        for x in s:
            g.add((a**x) % n)
        if g == s: #이면 a = generator
            results.append(a)
        return results

def main():
    # x = pow(2,11)-100
    # y = pow(2,11)
    # primeList = primesInRange(x, y)
    # p = primeList[-1]
    # q = primeList[-2]
    p, q = factorint(16695347)  #n = p*q
    print("primeNumber p: ", p)
    print("primeNumber q: ", q)
    bobPublicKey, bobPrivateKey = genRSAKeys(p, q)
    print("bob's Public Key (n, e): ", bobPublicKey)
    print("bob's Private Key (n, d): ", bobPrivateKey)

    ### RSADecrypt
    ciphertext = [1221847, 4795448, 11929767, 5886852, 2157475, 15309133, 12762586, 16082646, 3766899, 5637406, 2157475, 3983004, 7526959, 2157475, 8992392, 7362759, 7362759, 15309133, 5856642, 7526959, 3766899, 15087685, 15309133, 12762586, 14627653, 3766899, 5637406, 16082646, 12762586, 14627653, 3983004, 5856642, 8366708, 8366708, 3766899, 6004314, 4795448, 10888581, 10888581, 3983004, 3766899, 5136555, 3983004, 2157475, 10888581, 15741778, 8366708, 8366708]
    print("ciphertext: ", ciphertext)
    decrypt = RSADecryptSimpleString(ciphertext, bobPrivateKey)
    print("plaintext: ", decrypt)

if __name__ =="__main__":
    main()
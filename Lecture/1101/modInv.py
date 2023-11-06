import random
from RSA_Simple_String import findGenerators, primesInRange, eularPhi

def gcd(a, b):   # 최대공약수 체크 함수
    while (b != 0):
        temp = a % b
        a = b
        b = temp
    return abs(a)

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

def tot_list(n):
    phi = []
    x = 1
    while x < n:
        if gcd(x, n) == 1:
            phi += [x]
        x += 1
    return phi

def isCoPrime(a, b):     # 서로소 체크 함수
    if gcd(a, b) == 1:
        return True
    else:
        return False


print(modinv(5, 21))

print(( 5 * 17 ) % 21)

print(tot_list(10))


p = 23
q = 37
e = random.choice([x for x in range(1, (p-1)*(q-1)) if isCoPrime(x, (p-1)*(q-1))])
print(e)
d = modinv(e, (p-1)*(q-1))
print(d)

#####
# x = pow(2,10)
# y = pow(2,11)
# sharedPrime = 17 ## prime number
# primeList = primesInRange(x, y)
# sharedPrime = random.choice(primeList)
# print("Selected Prime", sharedPrime)
# sharedBase = random.choice(findGenerators(sharedPrime))  ### generator select...
# print("Selected Generator", sharedBase)
#
# aliceSecret = int(input("Alice's Secret: "))
# bobSecret = int(input("Bob's Secret: "))
#
# # Alice Sends Bob A = g^a mod p
# #A = (sharedBase**aliceSecret) % sharedPrime
# A = pow(sharedBase, aliceSecret, sharedPrime)
#
# # Bob Sends Alice B = g^b mod p
# B = (sharedBase ** bobSecret) % sharedPrime
#
# # Alice Computes Shared Secret: s = B^a mod p
# aliceSharedSecret = (B ** aliceSecret) % sharedPrime
#
# # Bob Computes Shared Secret: s = A^b mod p
# bobSharedSecret = (A ** bobSecret) % sharedPrime
#
# if aliceSharedSecret == bobSharedSecret:
#     print("Key Sharing Success!!!")
#     print("Shared Key:", aliceSharedSecret)
# else:
#     print("Wrong Key Sharing!!!")

x = pow(2,5)
y = pow(2,6)
primeList = primesInRange(x, y)
p = random.choice(primeList)
q = random.choice(primeList)
n = p*q
print(eularPhi(n)) ### 기약잉여계 집합의 원소 개수...
print((p-1)*(q-1)) ### 동일한 값...
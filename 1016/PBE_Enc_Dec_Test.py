import binascii
import hmac

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA512

SALT_SIZE = 16
BLOCK_SIZE = 16
KEY_SIZE = 32  # 32bytes


def aesEncrypt(message, key, iv):
    cipher = AES.new(key, AES.MODE_OFB, iv)
    return cipher.encrypt(message)


def aesDecrypt(encrypted, key, iv):
    cipher = AES.new(key, AES.MODE_OFB, iv)
    return cipher.decrypt(encrypted)


def generateKEK(salt, alicePassword):
    temp = salt + alicePassword
    hashObject = SHA512.new()
    hashObject.update(temp)
    KEK = hashObject.digest()
    print("key KEK: ", KEK.hex())
    return KEK[:KEY_SIZE]  # 전체 512비트 -> 그중 256비트 = 32바이트만 사용


def generateCEK():
    CEK = Random.new().read(KEY_SIZE)
    return CEK


def aesEncForMSG(plaintext, CEK, iv):
    ciphertext = aesEncrypt(plaintext, CEK, iv)
    return ciphertext


def aesEncForCEK(CEK, KEK, iv):
    encyptedCEK = aesEncrypt(CEK, KEK, iv)
    return encyptedCEK


def store_USB(salt, encryptedCEK, iv, encryptedPlainText):
    filename = input("USB Stored Filename (ex: PBE_Store.enc):")
    f = open(filename, 'wt')
    hpk = binascii.hexlify((salt)) + '$*****%'.encode('utf8') \
          + binascii.hexlify((salt)) + '$*****%'.encode('utf8') \
          + binascii.hexlify((salt)) + '$*****%'.encode('utf8') \
          + binascii.hexlify((salt)) + '$*****%'.encode('utf8')
    f.write(hpk)
    f.close()

def PBE_Encrypt():
    alicePassword, plaintext = getInput()
    # SHA generate --> generate KEK
    salt = Random.new().read(SALT_SIZE)
    iv = Random.new().read(BLOCK_SIZE)
    KEK = generateKEK(salt, alicePassword)  # input : salt, alicePassword  output : KEK
    # using random --> generate CEK
    CEK = generateCEK()
    # message AES Encryption using CEK
    encryptedPlainText = aesEncForMSG(plaintext, CEK, iv)  # parameter 1: 암호화 대상, parameter 2: 사용하는 키, parameter 3: iv
    # CEK AES Encryption using KEK
    encryptedCEK = aesEncForCEK(CEK, KEK, iv)  # parameter 1: 암호화 대상, parameter 2: 사용하는 키, parameter 3: iv
    # Generate File on USB
    store_USB(salt, encryptedCEK, iv, encryptedPlainText)


def inputPW():
    return input("Input PW : ").encode('utf-8')


def inputPlaintext():
    return input("Input plaintext : ").encode('utf-8')


def getInput():
    # inputPassword
    alicePassword = inputPW()
    # inputPlaintext
    plaintext = inputPlaintext()
    return alicePassword, plaintext


def PBE_Decrypt():
    pass


def main():
    getInput()
    PBE_Encrypt()
    PBE_Decrypt()


if __name__ == "__main__":
    main()

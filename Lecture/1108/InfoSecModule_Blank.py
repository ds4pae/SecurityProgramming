import base64

from Crypto import Random
from Crypto.Hash import SHA1, SHA512, SHA256
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import HMAC

def B64Encoding(data):
    b64data = base64.b64encode(data)
    return b64data


def B64Decoding(b64data):
    data = base64.b64decode(b64data)
    return data


def writeToFile(filename, data):
    output = B64Encoding(data)
    with open(filename, "wb") as file_pointer:
        file_pointer.write(output)
        file_pointer.close()


def readFromFile(filename):
    with open(filename, "rb") as file_pointer:
        readData = file_pointer.read()
        file_pointer.close()
    readData = B64Decoding(readData)
    return readData


def inputPlaintextAndGenKey_IV(KEY_SIZE, BLOCK_SIZE):
    plaintext = input("Input Plaintext: ")
    plaintext = plaintext.encode('utf-8')
    key = Random.new().read(KEY_SIZE)
    print("AES KEY: ", key)
    iv = Random.new().read(BLOCK_SIZE)
    print("AES IV: ", iv)
    return plaintext, key, iv


def generateHMAC(secret, message):
    hmacObj = HMAC.new(secret, digestmod=SHA256)
    hmacObj.update(message)
    print("HMAC: ", hmacObj.digest())
    return hmacObj.digest()


def verifyHMAC(secret, message, macCode):
    hmacObj = HMAC.new(secret, digestmod=SHA256)
    hmacObj.update(message)
    try:
        hmacObj.verify(macCode)   ## .hexverify() 함수를 이용할 경우에는 macCode.hex()로 변경하면 됨...
        print("The message '%s' is authentic" % message)
        return True
    except ValueError:
        print("The message or the key is wrong")
        return False


def genRSAKeys(bitsLength, name):
    keyObj = RSA.generate(bitsLength)   # p, q, n
    privateKey = keyObj.exportKey('PEM')   # private key 생성
    print(name, "의 개인키: ", privateKey)
    publicKey = keyObj.publickey().exportKey('PEM')     # public key 생성
    print(name, "의 공개키: ", publicKey)
    return privateKey, publicKey


def rsaEncrypt(message, publicKey):
    pubKey = RSA.importKey(publicKey)   # publicKey 바이트 스트림 --> (n, e) 추출...
    rsaEncObj = PKCS1_OAEP.new(pubKey)     # (n, e) 추출된 pubKey를 이용해서 RSA 암호화 객체 생성
    output = rsaEncObj.encrypt(message)
    print("RSA Encrypt: ", output)
    return output


def rsaDecrypt(received, privateKey):
    priKey = RSA.importKey(privateKey)    # privateKey 바이트 스트림 --> (n, d) 추출...
    rsaDecObj = PKCS1_OAEP.new(priKey)
    output2 = rsaDecObj.decrypt(received)
    print("RSA Decrypt: ", output2)
    return output2


def rsaDigSignGen(message, priKey):
    hashMsgObj = SHA512.new()
    hashMsgObj.update(message)
    privateKey = RSA.importKey(priKey)
    signGenFuncObj = PKCS1_v1_5.new(privateKey)  # privateKey를 이용하여 디지털 서명 객체 생성
    signMsg = signGenFuncObj.sign(hashMsgObj)  # message의 해시 객체에 대한 서명 과정 진행
    return signMsg


def rsaDigSignVerify(signMsg, message, pubKey):
    hashMsgObj = SHA512.new(message)   # hashMsgObj = SHA512.new(); hashMsgObj.update(message)
    publicKey = RSA.importKey(pubKey)
    signVerifyFuncObj = PKCS1_v1_5.new(publicKey)
    if signVerifyFuncObj.verify(hashMsgObj, signMsg):  # 서명값에 대한 일치 여부 검증(체크)
        return True
    else:
        return False


def aesEncrypt(key, iv, plaintext):
    aesEncObj = AES.new(key, AES.MODE_OFB, iv)
    output = aesEncObj.encrypt(plaintext)
    print("AES Encrypt(hex):", output.hex())
    return output


def aesDecrypt(key, iv, ciphertext):
    aesDecObj = AES.new(key, AES.MODE_OFB, iv)
    output = aesDecObj.decrypt(ciphertext)
    print("AES Decrypt:", output)
    return output


def aesEncWithHash(key, iv, plaintext):
    hashObject = SHA1.new(plaintext)
    plaintextWithHash = hashObject.hexdigest().encode() + plaintext
    output = aesEncrypt(key, iv, plaintextWithHash)
    return output


def aesDecWithHash(key, iv, received):
    output2 = aesDecrypt(key, iv, received)
    hash1 = output2[0:SHA1.digest_size*2]  # *2 를 하는 이유 : 위에서 hashObject.hexdigest() 즉, hexdigest() 형태로 생성하였기 때문에...
    hash2 = SHA1.new(output2[SHA1.digest_size*2:]) # plaintext에 대한 해시값 생성 객체
    if hash1 == hash2.hexdigest().encode(): # 동일하게 hexdigest() 로 해시값 비교...
        print("Hash Verification OK!!!")
        return output2[SHA1.digest_size*2:]  ### modified
    else:
        print("Integrity Error!!!!")
        return 0 ### modified




from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from Crypto import Random


def aesEncrypt(message, key, iv):
    cipherObject = AES.new(key, AES.MODE_OFB, iv)
    return cipherObject.encrypt(message.encode())

msg = "Hello"
key = b"01234567890123456789012345678912"
iv = Random.new().read(AES.block_size)
print(iv)
print(iv.hex())
print(AES.key_size)
print(AES.block_size)

cipherObject = AES.new(key, AES.MODE_OFB, iv)
output = iv + cipherObject.encrypt(msg.encode())
print(output)

######
### output, key, iv

iv = output[:16]
receivedCipher = output[16:]
decryptObject = AES.new(key, AES.MODE_OFB, iv)
plaintext = decryptObject.decrypt(receivedCipher)
print(plaintext.decode())

def aesDecrypt(message, key, iv):
    decryptObject = AES.new(key, AES.MODE_OFB, iv)
    return decryptObject.decrypt(message).decode()

######
msg = "Hello"
token = "World"
hash = SHA512.new()
hash.update(token.encode())
print(hash.digest())
key = hash.digest()[:32]
iv = hash.digest()[32:48]
print(key)
print(iv)

cipherObject = AES.new(key, AES.MODE_OFB, iv)
output = iv + cipherObject.encrypt(msg.encode())
print(output.hex())

####
token = input("Input Token for AES key &IV: ")
hash = SHA512.new()
hash.update(token.encode())
key = hash.digest()[:32]
iv = hash.digest()[32:48]
if iv == output[:16]:
    receivedCipher = output[16:]
    decryptObject = AES.new(key, AES.MODE_OFB, iv)
    plaintext = decryptObject.decrypt(receivedCipher)
    print("Decrypted :", plaintext.decode())
else:
    print("Wrong token!!!")
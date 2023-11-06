from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

rsa = RSA.generate(2048)

privateKey = rsa.export_key('PEM')
print(privateKey)   # RSA Private Key

publicKey = rsa.public_key()
print(publicKey.export_key('PEM'))    # RSA Public Key

message = b"Hello World!!!"

rsaObj = PKCS1_OAEP.new(publicKey)
encMSG = rsaObj.encrypt(message)
print()
print(encMSG)

privateKeyObj = RSA.importKey(privateKey)
rsa0bj2 = PKCS1_OAEP.new(privateKeyObj)
decMSG = rsa0bj2.decrypt(encMSG)
print()
print(decMSG.decode('utf-8'))
from Crypto import Random

from AES_with_SHA import aesEncrypt, aesDecrypt
from RSA_and_DigSign import rsaDigSignVerify, rsaDigSignGen
from RSA_and_DigSign import gen_RSA_Key


def main():
    BLOCK_SIZE = 16
    KEY_SIZE = 32
    message = b'Information security and Programming, Test Message!!! Name : Brother!!!'
    print("Message: ", message.decode())

    key = Random.new().read(KEY_SIZE)
    iv = Random.new().read(BLOCK_SIZE)

    print("AES Key: ", key.hex())
    print("IV: ", iv.hex())

    print("\n**RSA Key Pairs(priKey, pubKey) Generation")
    alice_priKey, alice_pubKey = gen_RSA_Key("Alice")
    bob_priKey, bob_pubKey = gen_RSA_Key("Bob")

    ####
    #### Alice : digital Signature Generation & AES Encryption
    signature = rsaDigSignGen(message, alice_priKey)
    print("Length of Signature: ", len(signature))
    encrypted = aesEncrypt(signature+message, key, iv)
    print("AES Encryption E(Sign(H(M))+M): ", encrypted.hex())
    print("Length of Encrypted(Sign(H(M))+M): ", len(encrypted))
    print("Sending: ", encrypted.hex())
    print("**** Alice : Sending Encrypted Message...\n\n")

    ####
    #### bob : AES Decryption & Digital Signature verification
    print("**** Bob : Receiving Encrypted Message...")
    print("Received: ", encrypted.hex())
    decryptedTemp = aesDecrypt(encrypted, key, iv)
    print("AES Decryption D(E(Sign(H(M))+M)): ", decryptedTemp.hex())

    decryptedSign = decryptedTemp[:256]
    print("Decrypted Sign: ", decryptedSign.hex())
    decryptedMsg = decryptedTemp[256:]
    print("Decrypted Message: ", decryptedMsg.decode())

    if rsaDigSignVerify(decryptedSign, decryptedMsg, alice_pubKey):     ## 만일 잘못 설정시...
        print("Digital Signature Verification OK!!!")
    else:
        print("Digital Signature Verification Fail!!!")


if __name__ == "__main__":
    main()

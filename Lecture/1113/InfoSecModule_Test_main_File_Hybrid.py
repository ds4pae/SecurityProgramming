from InfoSecModule import *


def HybridEnc(plaintext, publicKey, filename):
    KEY_SIZE = 32
    BLOCK_SIZE = 16
    sessionKey = Random.new().read(KEY_SIZE)
    iv = Random.new().read(BLOCK_SIZE)
    aesCiphertext = aesEncrypt(sessionKey, iv, plaintext)
    #aesCiphertext = aesEncWithHash(sessionKey, iv, plaintext)
    rsaCiphertext = rsaEncrypt(sessionKey, publicKey)
    print("rsaCipher length:", len(rsaCiphertext))
    output = iv +  '$*****$'.encode('utf8') + rsaCiphertext + '$*****$'.encode('utf8') + aesCiphertext
    writeToFile(filename, output)


def HybridDec(privateKey, filename):
    readData = readFromFile(filename)
    iv, rsaCiphertext, aesCiphertext = readData.split('$*****$'.encode('utf8'))
    print("aesCiphertext: ", aesCiphertext)
    decrypted_sessionKey = rsaDecrypt(rsaCiphertext, privateKey)
    decrypted_plaintext = aesDecrypt(decrypted_sessionKey, iv, aesCiphertext)
    #decrypted_plaintext = aesDecWithHash(decrypted_sessionKey, iv, aesCiphertext)
    print("plaintext: ", decrypted_plaintext.decode())


def main():
    ## Hybrid Enc/Dec
    ## Alice의 공개키/개인키 쌍 생성
    alice_privateKey, alice_publicKey = genRSAKeys(2048, "Alice")
    writeToFile("alice_privateKey.pem", alice_privateKey)
    writeToFile("alice_publicKey.pem", alice_publicKey)
    ## Bob의 공개키/개인키 쌍 생성
    bob_privateKey, bob_publicKey = genRSAKeys(2048, "Bob")
    writeToFile("bob_privateKey.pem", bob_privateKey)
    writeToFile("bob_publicKey.pem", bob_publicKey)

    ## 암호화하고자 하는 메시지 입력
    plaintext = input("Hybrid Enc/Dec - Input Plaintext: ").encode('utf8')

    ## 암호화된 값이 저장될 파일
    alice_output_filename ="alice_hybrid_output.bin"
    bob_publicKey = readFromFile("bob_publicKey.pem")
    HybridEnc(plaintext, bob_publicKey, alice_output_filename)
    ## Alice --> Bob : "alice_hybrid_output.bin" 파일 전송

    ## Bob : "alice_hybrid_output.bin" 파일 수신 후 복호화 과정 수행
    bob_privateKey = readFromFile("bob_privateKey.pem")
    HybridDec(bob_privateKey, alice_output_filename)


if __name__ == "__main__":
    main()

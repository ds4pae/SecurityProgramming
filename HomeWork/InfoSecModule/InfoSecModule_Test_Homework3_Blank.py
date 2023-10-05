from InfoSecModule import *

def HybridEnc(plaintext, publicKey, filename):
    KEY_SIZE = 32
    BLOCK_SIZE = 16
    sessionKey = Random.new().read(KEY_SIZE)
    iv = Random.new().read(BLOCK_SIZE)
    aesCiphertext = aesEncrypt(???, iv, plaintext)
    rsaCiphertext = rsaEncrypt(???, publicKey)
    print("rsaCipher length:", len(rsaCiphertext))
    output = iv +  '$*****$'.encode('utf8') + rsaCiphertext + '$*****$'.encode('utf8') + aesCiphertext
    writeToFile(filename, output)


def HybridDec(privateKey, filename):
    readData = readFromFile(filename)
    iv, rsaCiphertext, aesCiphertext = readData.split(???)
    print("aesCiphertext: ", aesCiphertext)
    decrypted_sessionKey = rsaDecrypt(???, privateKey)
    decrypted_plaintext = aesDecrypt(???, iv, aesCiphertext)
    print("plaintext: ", decrypted_plaintext.decode())

def main():
    ## Hybrid Enc/Dec
    plaintext = input("Hybrid - Input Plaintext: ").encode()
    bob_privateKey = b'-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEAi06y3N8X/J3jzOriH5zMSIeFr5sEIrkr9OA5wqE/32PNJ4NE\n/tyCyPMPD+51cINOEAXvMTz7duBQreyDL3xDCQ+rgppQc4IQFqdSlcHXdxM+vDpB\nO0Kdvz1X9cmIylVMIYytYeskbL3KoiqtB0zBmV8S8rlNmwSI9pZ+GBkGwOFD6zmv\nvqx1gHxQE1PJhENoLIYUkzzIAUkLn7j7ILzQvdLvtIovh+3iYeFhF4T1lhrtpNjn\nWKmcK8VEDzhTNrOATcZefifOn1hSasJSiteEVe+Uq59xbvveqk1NPYtW3YInyAkc\nnmjT0JtRO3ZmqTO0A3rbg3sgrVI4YjdPdqEc1QIDAQABAoIBAAeyf6027HyKUtcf\nQVhNfHd4ztkJn9xf+T73Zr72KZvTyAxUs1VruhRADdyA/gngpMm7h4sOcLc8T2jq\nG8OIwlbNVVo1jELISdBJStsN0gnOd+sZmEId0lk0mq1w3Hc66FEllJec+68V0OJN\n/lqGvLRsmD+YyozJXtyqgGl0yeE9XEwE0EKbkoKJEHNojquWQR4wYhn5se5R0bPV\nOdNh53Au23AmF7DV/qaPFTOgc6vMtsmXXUdHDJ4qnzxXeV7f4mT2kiBLfYcslqqT\ntWhzGu4U0LkdX37TcyW02vh1cBoAx8Gc6Bx4bApguxC52rd9A1b8j3X9kfS9L6dP\nu87JijECgYEAtksZFBj0x33FOdj2EHPptmqdo/v5xTCgA2UACl0M+30ipgSp8RAm\nvu9lqlZn63hb/oNod0BYjiCNF3sgRWHJ9BcnFug0DpuAUTGpPUBIq6kn2vBOfu6r\n7NrF7kYHTCFmJFLvfO/8GRJBc/ONeEaAIfQffza+fpN2ffJSvtcq8A0CgYEAw6Ix\nfAdJ/8wxJLv5TmXWmUb69AkVg2i4ZSLSFccQYV1qzyjbdbivz1biPTzU1qHTKJum\nLPWqGml8lDJv2sPSQhOPSMwMq8LLtAkUv4zPe3ktwLxJkEeGLoDhQm5KZbZVIP36\ngH1iH9clXYB+2E3pmxXhM9i5MkxBDeGmWDHV5ekCgYAuoHjSrit2F1JqIHeX774Y\n3Z5iwmG5sV1MYPoorHJUpUZGhqzdLw9qCRvM/PrpvMhzCjOfRQMhn2vXVLQFayTX\n3VAvSMd/8QBaRESQmS+9ULAUDSFW0D+DftXfw2O8clKI+fmt0EiANS4utV47JHVD\nugiQZnVFNPy67E+D5s9hxQKBgCcDGBUgqvwMrxwhNBUTL9k/E1pI2XZsEqFwcS6Q\nlM6lv1/ySNlP7BdPvyvxDoyClsY5S8kZcEN2F7bB3BZnCG3O0rr0ne4+mTqcuPt9\ny/5Wau5NXeocqUBqyQDjV4iy9ITwwNyQpFmvIK9lqWXfG5+mnFMne77w/+QRxIc/\n4OTJAoGAWYZY+4+soMPmfWFqG7n4+dTvsCixF3WfuBhvBg+aXCvkwgFucxMNZWdD\n7wAADHwdetopt71LI7MWxfBu3g57e4qDJEhpYOqXxaT/+Fok0vAa9sQAyO4QBWgV\n1d2RWFg5cw5JfUdbJr50Gk3Tp0i54EYo38RDSodXK5vkfjdZRJk=\n-----END RSA PRIVATE KEY-----'
    bob_publicKey = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAi06y3N8X/J3jzOriH5zM\nSIeFr5sEIrkr9OA5wqE/32PNJ4NE/tyCyPMPD+51cINOEAXvMTz7duBQreyDL3xD\nCQ+rgppQc4IQFqdSlcHXdxM+vDpBO0Kdvz1X9cmIylVMIYytYeskbL3KoiqtB0zB\nmV8S8rlNmwSI9pZ+GBkGwOFD6zmvvqx1gHxQE1PJhENoLIYUkzzIAUkLn7j7ILzQ\nvdLvtIovh+3iYeFhF4T1lhrtpNjnWKmcK8VEDzhTNrOATcZefifOn1hSasJSiteE\nVe+Uq59xbvveqk1NPYtW3YInyAkcnmjT0JtRO3ZmqTO0A3rbg3sgrVI4YjdPdqEc\n1QIDAQAB\n-----END PUBLIC KEY-----'

    ## Alice --> Bob : 하이브리드 암호화
    alice_output_filename ="alice_hybrid_output.bin"
    HybridEnc(plaintext, ???, alice_output_filename)

    ## Bob : 하이브리드 복호화
    HybridDec(???, alice_output_filename)


if __name__ == "__main__":
    main()

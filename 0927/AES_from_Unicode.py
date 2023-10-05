import binascii

from AES_Test_New import aesEncrypt, aesDecrypt

def main():
    key = "8935496715d7f5b9d13f7d3a0468871e7a96c5312b7e7cb2d1f17ba081cfb9a3"
    IV = "64f3ed21013257597e56d482b6b4127e"
    ciphertext = "ecfdf6de5d586e2828b0a5329f46edc75273"

    key_bytearray = bytearray.fromhex(key)
    key_hex = binascii.hexlify(key_bytearray).decode()
    print(key_hex)

    plaintext = aesDecrypt(bytearray.fromhex(ciphertext), bytearray.fromhex(key), bytearray.fromhex(IV))
    print(plaintext)
    print("AES Decryption: ", plaintext.decode())

    #단답형 문제

    key = "fd9d4d5b7a8a8fae6b1bc099b799110f7e4338606e2610f5d9506a4346e0c3bf"
    IV = "fd9d4d5b7a8a8fae6b1bc099b799110f"
    ciphertext = "5fb162e3cfbf49258bd4d6c54f6f19024487abcab347a123cd7d1c13b4c691"
    plaintext = aesDecrypt(bytearray.fromhex(ciphertext), bytearray.fromhex(key), bytearray.fromhex(IV))

    print("AES Decryption: ", plaintext.decode())

if __name__ == "__main__":
    main()

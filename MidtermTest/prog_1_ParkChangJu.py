import random
from Crypto.Cipher import AES
from Crypto.Hash import SHA512
import string
from Etc.detectEnglish import isEnglish
import time

def aesEncrypt(message, key, iv):
    cipher = AES.new(key, AES.MODE_OFB, iv)
    return cipher.encrypt(message)

def aesDecrypt(encrypted, key, iv):
    cipher = AES.new(key, AES.MODE_OFB, iv)
    return cipher.decrypt(encrypted)

def gen_Key_IV(seed):
    hash = SHA512.new()
    hash.update(seed.encode('utf-8'))
    key = hash.digest()[16:48] # AES Key 값: seed로 부터 생성된 SHA512 해시 값의 16 바이트 ~ 47 바이트(32*8 = 256비트) 까지의 값만을 이용함
    iv = hash.digest()[:16]  # AES IV 값 : seed로 부터 생성된 SHA512 해시 값의 0 바이트 ~ 15 바이트(16*8 = 128비트) 까지의 값을 이용함
    return key, iv

# 아래 부분에 대해서는 개선(예시 : 순차 검색 등)이 필요함
def gen_Key_IV_from_Seed(seed_length, LETTERS_SET):
    seed = [ ]
    for i in range(seed_length):
         seed.append(str(LETTERS_SET[random.randrange(0, len(LETTERS_SET))])) # 랜덤 방식으로 seed_length에 해당하는 값을 생성한다
    seed = "".join(seed)
    key, iv = gen_Key_IV(seed)
    return key, iv, seed

def aesKeyGenWithSHAHack(ciphertext, seed_length, LETTERS_SET):
    count = 0
    key_set = set()
    start_time = time.time()

    while (True):
        count +=1
        key, iv, seed = gen_Key_IV_from_Seed(seed_length, LETTERS_SET)
        if key not in key_set:
            decrypted = aesDecrypt(ciphertext, key, iv)
            if (isEnglish(str(decrypted))):
                end_time = time.time()
                print("검색한 SEED : %s \t Key : %s \t IV : %s" %(seed, key.hex(), iv.hex()))
                print("decrypted: ", decrypted.decode('utf-8', errors='ignore'))  # 평문을 출력
                print(f"총 키 탐색 횟수 : {count}번")
                print(f"시간 : {end_time - start_time:.5f} sec")
                break
            else:
                key_set.add(key)

def main():
    ## 아래 seed 값을 이용해서 AES 암호화 과정에 사용될 Key와 IV 값을 생성한다.
    seed = "Sec"
    print("입력된 Seed 값: ", seed)
    msg = "Information Security Programming Test Message Hanshin University Computer Science."
    print("message: ", msg)
    key, iv = gen_Key_IV(seed)
    iv = b'0000000000123456'
    print("Seed로부터 생성된 Key: ", key.hex())
    print("Seed로부터 생성된 IV: ", iv.hex())
    ciphertext = aesEncrypt(msg.encode(), key, iv)
    print("ciphertext: ", ciphertext.hex())

    LETTERS_SET = string.ascii_letters
    print("LETTERS_SET: ", LETTERS_SET)
    seed_length = len(seed)
    print("\nSeed Hack 방식을 이용한 복호화 과정 수행중")
    aesKeyGenWithSHAHack(ciphertext, seed_length, LETTERS_SET)

if __name__ == "__main__":
    main()

import string
import random

def substituedEncryption(plaintext, dic, LETTERS):
    ciphertext = ""
    for key in plaintext:
        if key in LETTERS:
            temp = dic[key]  # 맵dic에서 key에 해당하는 value 값을 추출
            ciphertext += temp
        else:
            ciphertext += key
    return ciphertext

def substituedDecryption(ciphertext, dic, LETTERS):
    dic_swap = {value : key for key, value in dic.items()}
    for key, value in dic.items():
        dic_swap[value] = key

    decrypted = ""
    for key in ciphertext:
        if key in LETTERS:
            temp = dic_swap[key]
            decrypted += temp
        else:
            decrypted += key
    return decrypted

LETTERS = string.ascii_lowercase

# LETTERS는 순차적인 소문자, shuffled_letters은 무작위 순서의 소문자
shuffled_letters = "".join(random.sample(LETTERS, len(LETTERS)))

dic = {}
# 순차적임, 랜덤 값을 넣어주어야함
for i in range(len(LETTERS)):
    dic[LETTERS[i]] = shuffled_letters[i]

print(dic) # 생성 된 키 출력

#get user_input
plaintext = input("Input Plaintext : ")

#encryption
ciphertext = substituedEncryption(plaintext, dic, LETTERS)
print("ciphertext : " + ciphertext)

#decryption
decrypted = substituedDecryption(ciphertext, dic, LETTERS)
print("decrypted : " + decrypted)
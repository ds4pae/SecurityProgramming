import string
import random



LETTERS = string.ascii_letters
print(LETTERS)

key = random.randrange(0, len(LETTERS))

plaintext = "Hello World"

#caesar_Encryption
ciphertext = ""
for char in plaintext:

    # charIndexValue  = LETTERS.find(char)
    # endIndexValue = (charIndexValue + key) % len(LETTERS) #encryption
    # ciphertext += LETTERS[endIndexValue]

    if char in LETTERS:
        ciphertext += LETTERS[(LETTERS.find(char) + key) % len(LETTERS)]
    else:
        ciphertext += char
print(ciphertext)

#caesar_Decryption

decrypt = ""
for char in ciphertext:
    if char in LETTERS:
        decrypt += LETTERS[(LETTERS.find(char) - key) % len(LETTERS)]
    else:
        decrypt += char

print("decrypted text : " + decrypt)
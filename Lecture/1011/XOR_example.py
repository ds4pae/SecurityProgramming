key = "12345"
msg = "ABCDE"

ciphertext = []
plaintext = []
for (k, m) in zip(key, msg):
    ciphertext.append(chr(ord(k) ^ ord(m)))

output = "".join(ciphertext)
print(output)

for (k, m) in zip(key, output):
    plaintext.append(chr(ord(k) ^ ord(m)))

output = "".join(plaintext)
print(output)
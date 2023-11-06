from Crypto.Cipher import AES
import secrets

# 주어진 데이터
ciphertext = bytes.fromhex("3f2f77c9008962561c63a37862aa020fc7c816f42ef06db0efe5d97d0805dc16c217d0436ca43e39669e03f0a6a0350b5d6921f73df0a4b82a0170f069b134704c8da628b36b7a1fdb171230fc078313d16eaf5157")
iv = b'0000000000123456'

# AES 암호화를 위한 랜덤 키 생성
random_key = secrets.token_bytes(32)  # 32 바이트 랜덤 키 생성 (AES-256)

# AES 암호화 객체 생성
cipher = AES.new(random_key, AES.MODE_OFB, iv)

# 암호문 해독
plaintext = cipher.decrypt(ciphertext)

# 결과 출력
print("Random Key:", random_key)
print("Decrypted Plaintext (hex):", plaintext.hex())


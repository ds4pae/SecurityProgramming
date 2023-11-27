from Crypto.Hash import SHA512

block1 = { "INDEX" : 0,
           "판매자"  : "파이썬",
           "구매자" : "김철수",
           "개수" : "3개",
           "시간 " : "1990-01-01 00:00:00",
           "Previous Block" : None
}

block2 = { "INDEX" : 1,
           "판매자"  : "자바",
           "구매자" : "이철수",
           "개수" : "2개",
           "시간 " : "1991-01-01 00:00:00",
           "Previous Block" : SHA512.new( str(block1).encode() ).hexdigest()
}

block3 = { "INDEX" : 2,
           "판매자"  : "한신대",
           "구매자" : "박철수",
           "개수" : "5개",
           "시간 " : "1992-01-01 00:00:00",
           "Previous Block" : SHA512.new( str(block2).encode() ).hexdigest()
}

h = SHA512.new()
h.update(str(block1).encode())
print("SHA(block1) :", h.digest())
print("SHA(block1) :", h.digest().hex())

print(  SHA512.new( str(block1).encode() ).hexdigest() )
print(block1)
print(block2)
print(block3)


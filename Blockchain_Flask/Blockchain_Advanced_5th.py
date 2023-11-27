from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto.Signature import pkcs1_15
from InfoSecModule import *
import json
import time

## Add Digital Signature Data on Block
class Block:
    def __init__(self, index, previous_hash, timestamp, userName, data, nonce=0, signature=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.userName = userName
        self.data = data
        self.nonce = nonce
        self.signature = signature  ## 추가....
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.index}{self.previous_hash}{self.timestamp}{self.userName}{self.data}{self.nonce}"  ## 수정...
        return SHA512.new(data.encode()).hexdigest()

    ## 디지털 서명 생성 메소드 추가...
    def sign(self, privateKey):
        # Sign the block using the private key
        priKey = RSA.importKey(privateKey)
        signer = PKCS1_v1_5.new(priKey)
        h = SHA256.new(str(self.hash).encode())
        self.signature = signer.sign(h)
        #return self.signature

    ## 디지털 서명 검증 메소드 추가...
    def verify_signature(self, publicKey):
        # Verify the signature of the block using the public key
        pubKey = RSA.importKey(publicKey)
        verifier = PKCS1_v1_5.new(pubKey)
        h = SHA256.new(str(self.hash).encode())
        try:
            verifier.verify(h, self.signature)
            return True
        except (ValueError, TypeError):
            return False

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 0  # Number of leading zeros required in the hash
        self.privatekey, self.publicKey = self.generate_key_pair()   ## 필드값 추가.....

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), "User Name", "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    ### Blockchain에서 사용할 키쌍을 생성하는 메소드 추가...
    def generate_key_pair(self):
        # Generate a pair of RSA keys
        key = RSA.generate(2048)
        privateKey = key.exportKey()
        publicKey = key.publickey().export_key()
        return privateKey, publicKey

    def add_block(self, userName, data):
        # Add a new block to the blockchain
        index = len(self.chain)
        timestamp = int(time.time())
        previous_hash = self.get_latest_block().hash
        nonce = 0
        new_block = Block(index, previous_hash, timestamp, userName, data, nonce)
        new_block.sign(privateKey=self.privatekey)
        while not self.is_valid_proof(new_block):
            nonce += 1
            new_block.nonce = nonce
            new_block.hash = new_block.calculate_hash()

        self.chain.append(new_block)

    def mine_block(self, userName, data):    ## add block과 유사한 기능을 수행, 다만 동일한 해시값이 나오지 않도록 nonce 값 조정
        index = len(self.chain)
        previous_hash = self.get_latest_block().hash
        timestamp = int(time.time())
        nonce = 0

        new_block = Block(index, previous_hash, timestamp, userName, data, nonce)
        new_block.sign(privateKey=self.privatekey)  ## 추가....
        while not self.is_valid_proof(new_block):
            nonce += 1
            new_block.nonce = nonce
            new_block.hash = new_block.calculate_hash()

        self.chain.append(new_block)

    ## 아래 내용 수정 ....
    def is_valid_proof(self, block):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
            if not current_block.verify_signature(publicKey=self.publicKey):
                return False
        #target = "0" * self.difficulty
        #return block.hash[:self.difficulty] == target
        return True

    def getUserName(self):
        return Blockchain.get_latest_block().userName

    ## file로 쓰기/읽기 모듈 추가...
    def save_to_file(self, filename: str):
        # Save the entire blockchain to a file in JSON format
        with open(filename, 'w') as file:
            data = []
            for block in self.chain:
                block_data = {
                    'index': block.index,
                    'timestamp': block.timestamp,
                    'userName': block.userName,
                    'data': block.data,
                    'nonce': block.nonce,
                    'previous_hash': block.previous_hash,
                    'hash': block.hash
                }
                data.append(block_data)
            json.dump(data, file, indent=2)

    def load_from_file(self, filename: str):
        # Load the entire blockchain from a file in JSON format
        with open(filename, 'r') as file:
            data = json.load(file)
            self.chain = []
            for block_data in data:
                new_block = Block(
                    index=block_data['index'],
                    timestamp=block_data['timestamp'],
                    userName=block_data['userName'],
                    data=block_data['data'],
                    nonce=block_data['nonce'],
                    previous_hash=block_data['previous_hash']
                )
                new_block.hash = block_data['hash']
                self.chain.append(new_block)


def addPublicKeyOnBlockchain(my_blockchain, userName):
    privateKey, publicKey = genRSAKeys(2048, userName)
    publicKey = str(publicKey)
    #my_blockchain.mine_block(userName, publicKey)  # blockchain에 publicKey 저장
    my_blockchain.add_block(userName, publicKey)  # 수정 mine_block --> add_block
    with open(f"PrivateKey/{userName}_privateKey.pem", "wb") as f:
        f.write(privateKey)
        f.close()


def getPublicKeyFromBlockchain(my_blockchain, userName):
    for block in my_blockchain.chain:
        if my_blockchain.is_valid_proof(block):
            if (block.userName == userName):
                print("Valid Block")
                print(f"Block #{block.index} - Hash: {block.hash}")
                print(f"UserName: {block.userName} ")
                #print(f"Public Key: {block.data}")
                return block.data

    return None


if __name__ == '__main__':
    # Create a blockchain
    my_blockchain = Blockchain()

    addPublicKeyOnBlockchain(my_blockchain, "Alice")
    addPublicKeyOnBlockchain(my_blockchain, "Bob")
    addPublicKeyOnBlockchain(my_blockchain, "Carol")

    myPublicKey = getPublicKeyFromBlockchain(my_blockchain, "Alice")
    print(f"Public Key Stored on Blockchain: {myPublicKey}")

    my_blockchain_JSON_file = "my_blockchain_with_signature.json"  ## 수정....
    my_blockchain.save_to_file(my_blockchain_JSON_file)

    load_blockchain = Blockchain()
    load_blockchain.load_from_file(my_blockchain_JSON_file)

    yourPublicKey = getPublicKeyFromBlockchain(load_blockchain, "Carol")
    print(f"Public Key Stored on Blockchain: {yourPublicKey}")

    addPublicKeyOnBlockchain(load_blockchain, "David") ## 수정....
    new_blockchain_JSON_file = "my_blockchain_with_signature_new.json"  ## 수정....
    load_blockchain.save_to_file(new_blockchain_JSON_file)





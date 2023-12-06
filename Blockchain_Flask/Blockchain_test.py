from Crypto.Hash import SHA512
import time
from multipledispatch import dispatch
from InfoSecModule import *
import json

class Block:
    # 필드값 : self.
    # 생성자 : self.
    def __init__(self, index, previous_hash, timestamp, userName, data, nonce = 0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.userName = userName  # userName ....
        self.data = data   # userName's public key ????
        self.nonce = nonce
        self.hash = self.calculate_Hash()

    # 메소드 : self.
    def calculate_Hash(self):
        value = f"{self.index}{self.previous_hash}{self.timestamp}{self.userName}{self.nonce}{self.data}"
        return SHA512.new(value.encode()).hexdigest()

    def get_Hash(self):
        return self.hash

    def get_value(self):
        return 0

    def set_Value(self, num):
        self.num = num

    def print_Block(self):
        print(f"""
            Block # : {self.index}, Previous_Hash : {self.previous_hash}
            TimeStamp : {self.timestamp}, 
            Data : {self.data},
            Hash : {self.hash}
        """)

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]  #### blockchain.....

    def create_genesis_block(self):
        return Block(0, 0, int(time.time()), "MyBlock", "Genesis Block", 0)

    @dispatch(Block)
    def add_block(self, new_Block):
        new_Block.previous_hash = self.get_last_block().hash
        new_Block.hash = new_Block.calculate_Hash()
        self.chain.append(new_Block)

    @dispatch(str, str)
    def add_block(self, userName, data):
        index = self.get_last_block().index + 1
        previous_hash = self.get_last_block().hash
        timestamp = int(time.time())
        nonce = 0
        self.chain.append(Block(index, previous_hash, timestamp, userName, data, nonce))

    def get_last_block(self):
        return self.chain[-1]

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            data = [ ]
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
            json.dump(data, file, indent=4)
            file.close()

    def load_from_file(self, filename):
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
            file.close()

def main():

    # my_blockchain = Blockchain()  ####
    #
    # my_first_block = Block(1, my_blockchain.get_last_block().hash, int(time.time()), "Bob", "Bob's public Key", 0)
    # my_first_block.print_Block()
    # my_second_block = Block(2, my_blockchain.get_last_block().hash, int(time.time()), "Alice", "Alice's public key :: !!@FEREWFEFFDSFSDAFSDFASFSADFSFDDSFDSFFDSFDSAFFRFRE", 0)
    # my_second_block.print_Block()
    #
    # my_blockchain.add_block(my_first_block)
    # my_blockchain.add_block(my_second_block)
    #
    # userName = "Carol"
    # privateKey, publicKey = genRSAKeys(2048, userName)   ## bytes...
    # publicKeyBase64 = base64.b64encode(publicKey)
    #
    # my_blockchain.add_block(userName, publicKeyBase64.decode())
    #
    # my_blockchain.save_to_file("./my_blockchain_test.json")
    #
    # ## 블록체인 내부 검색 방법.....
    # for block in my_blockchain.chain:    # my_blockchain.chain --> self.chain 인 [ ] 리스트...
    #     if block.userName == "Carol":
    #         print(f"Carol's Public Key : {block.data}")
    #
    my_blockchain = Blockchain()

    my_blockchain.load_from_file("./my_blockchain_test.json")
    userName = "Lee Kang In"
    privateKey, publicKey = genRSAKeys(2048, userName)  ## bytes...
    publicKeyBase64 = base64.b64encode(publicKey)
    my_blockchain.add_block(userName, publicKeyBase64.decode())
    my_blockchain.save_to_file("./my_blockchain_test.json")

    for block in my_blockchain.chain:    # my_blockchain.chain --> self.chain 인 [ ] 리스트...
        if block.userName == userName:    ### "Hong Gil Dong"
            print(f"Lee Kang In's Public Key : {block.data}")
            hgd_publicKey = block.data
            break

    plaintext = "Hello World".encode()  ## bytes....
    publicKey = base64.b64decode(hgd_publicKey)
    ciphertext = rsaEncrypt(plaintext, publicKey)
    print(f"ciphertext : {ciphertext}")

    decMSG = rsaDecrypt(ciphertext, privateKey)
    print(f"decrypted message: {decMSG.decode()}")


if __name__ == "__main__":
    main()
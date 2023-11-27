from Crypto.Hash import SHA512
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, userName, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.userName = userName
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = f"{self.index}{self.previous_hash}{self.timestamp}{self.userName}{self.data}{self.nonce}"
        return SHA512.new(data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 0  # Number of leading zeros required in the hash

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), "User Name", "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def mine_block(self, userName, data):
        index = len(self.chain)
        previous_hash = self.get_latest_block().hash
        timestamp = int(time.time())
        nonce = 0

        new_block = Block(index, previous_hash, timestamp, userName, data, nonce)

        while not self.is_valid_proof(new_block):
            nonce += 1
            new_block.nonce = nonce
            new_block.hash = new_block.calculate_hash()

        self.chain.append(new_block)

    def is_valid_proof(self, block):
        target = "0" * self.difficulty
        return block.hash[:self.difficulty] == target

    def getUserName(self):
        return Blockchain.get_latest_block().userName


if __name__ == '__main__':
    # Create a blockchain
    my_blockchain = Blockchain()

    # Mine some blocks
    my_blockchain.mine_block("Alice", "Transaction Data 1")
    my_blockchain.mine_block("Bob", "Transaction Data 2")
    my_blockchain.mine_block("Carol","Transaction Data 3")

    # Print the blockchain
    for block in my_blockchain.chain:
        print(f"Block #{block.index} - Hash: {block.hash}")
        print(f"UserName #{block.userName} - Data:{block.data}")
        if my_blockchain.is_valid_proof(block):
            print("Valid Block")
        else:
            print("Invalid!!!")

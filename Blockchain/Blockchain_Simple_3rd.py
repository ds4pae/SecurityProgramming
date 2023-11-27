import datetime
from Crypto.Hash import SHA512

class Blockchain(object):
    def __init__(self):
        self.block_count =0
        self.chain = [ ]
        self.current_transaction = [ ]

    def new_transaction(self, sender, recipient, amount):
        self.current_transaction.append(
            {
                "sender" : sender,
                "recipient" : recipient,
                "amount" : amount,
                "timestamp" : datetime.datetime.now().timestamp()
            }
        )
        return self.last_block()

    def new_block(self, proof, previous_hash=None):
        block = {
            "index" : len(self.chain) +1,
            "timestamp" : datetime.datetime.now().timestamp(),
            "transactions" : self.current_transaction
        }

        self.current_transaction = []
        self.chain.append(block)
        return block

    def last_block(self):
        return self.chain[-1]

    def get_chain_length(self):
        self.block_count += 1
        return self.block_count


sample_blockchain = Blockchain()
sample_blockchain.new_block(proof= "1")
print(sample_blockchain.chain)

sample_blockchain.new_block(proof= "1")
print(sample_blockchain.chain)

sample_blockchain.new_transaction(sender="김민수", recipient="박철수", amount=10)
sample_blockchain.new_block(proof= "1")
print(sample_blockchain.chain)

sample_blockchain.new_transaction(sender="이민수", recipient="이철수", amount=5)
sample_blockchain.new_block(proof= "1")
print(sample_blockchain.chain)

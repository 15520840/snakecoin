import hashlib as hasher
import datetime as date
from flask import Flask
from flask import request
import json
import requests

node = Flask(__name__)


class Block:
        def __init__(self, index, timestamp, data, previous_hash):
                self.index = index
                self.timestamp = timestamp
                self.data = data
                self.previous_hash = previous_hash
                self.hash = self.hash_block()

        def hash_block(self):
                sha = hasher.sha256()
                sha.update((str(self.index) +
                           str(self.timestamp) +
                           str(self.data) +
                           str(self.previous_hash)).encode())

                return sha.hexdigest()


def create_genesis_block():
        # Manually create block with index 0 and arbitrary previous hash
        return Block(0, date.datetime.now(), {
                "proof-of-work": 9,
                "transactions": None,
        }, "0")

miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"

blockchain = []
blockchain.append(create_genesis_block())
this_nodes_transactions = []

@node.route('/mine', methods = ['GET'])
def mine():
        # Get the last proof of work
        last_block = blockchain[len(blockchain) - 1]
        last_proof = last_block.data['proof-of-work']

        # Find the proof of work for current block being mined
        # The program will hang here until a new proof of work found
        proof = proof_of_work(last_proof)
        this_nodes_transactions.append(
                {"from": "network", "to": "miner_address", "amount": 1}
        )

        # Create new data block
        new_block_data = {
                "proof-of-work": proof,
                "transactions": list(this_nodes_transactions)
        }

        new_block_index = last_block.index + 1
        new_block_timestamp = this_timestamp = date.datetime.now()
        last_block_hash = last_block.hash

        # Empty transaction list
        this_nodes_transactions[:] = []

        mined_block = Block(
                new_block_index,
                new_block_timestamp,
                last_block_hash
        )

        blockchain.append(mined_block)

        # Let the client know we mined a block
        return json.dump(
                {
                        "index": new_block_index,
                        "timestamp": str(new_block_timestamp),
                        "data": new_block_data,
                        "hash": last_block_hash
                }
        ) + "\n"

@node.route('/blocks', methods = ['GET'])
def get_blocks():
        chain_to_send = blockchain

        for block in chain_to_send:
                block_index = str(block.index)
                block_timestamp = str(block.timestamp)
                block_data = str(block.data)
                block_hash = block.hash

                block = {
                        "index": block_index,
                        "timestamp": block_timestamp,
                        "data": block_data,
                        "hash": block_hash
                }

        # Send our chain to whomever requested it
        chain_to_send = json.dumps(chain_to_send)
        return chain_to_send

def find_new_chains():
        # Get the blockchain of every other node
        other_chains = []
        for node_url in peer_nodes:
                block = requests.get(node_url + "/blocks").content
                # Convert JSON object to python dictionaries
                block = json.load(block)
                other_chains.append(block)

        return other_chains

def consensus():
        # Get the blocks from other nodes
        other_chains = find_new_chains()

        longest_chain = blockchain

        for chain in other_chains:
                if len(longest_chain) < len(chain):
                        longest_chain = chain

        blockchain = longest_chain



def proof_of_work(last_proof):
        incrementor = last_proof + 1

        while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
                incrementor += 1

        return incrementor

@node.route('/txion', methods = ['POST'])
def transaction():
        # On each new POST request, we extract the transaction data
        new_txion = request.get_json()
        this_nodes_transactions.append(new_txion)

        print("New transaction")
        print("From: {}".format(new_txion['from']).encode())
        print("To: {}".format(new_txion['to']).encode())
        print("Amount: {}\n".format(new_txion['amount']))

        return "Transaction submission successful\n"



def next_block(last_block):
        this_index = last_block.index + 1
        this_timestamp = date.datetime.now()
        this_data = "Hey, I'm block" + str(this_index)
        this_hash = last_block.hash

        return Block(this_index, this_timestamp, this_data, this_hash)

# Create blockchain and genesis block
previous_block = blockchain[0]

# Number of blocks to add after genesis block
num_of_blocks_to_add = 20

# Add block to the chain
for i in range(0, num_of_blocks_to_add):
        block_to_add = next_block(previous_block)
        blockchain.append(block_to_add)
        previous_block = block_to_add

        # Broadcast this
        print("Block #{} has been added to the blockchain".format(block_to_add.index))
        print("Hash: {}\n".format(block_to_add.hash))


node.run()

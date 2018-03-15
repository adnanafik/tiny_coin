from flask import Flask
from flask import request
from hashlib import sha256
import datetime as date
import random
import uuid
import json
import requests

from block.block import Block
from chain.chain import Chain
from utils.utils import *


node = Flask(__name__)

#this node random miner address
miner_address = uuid.uuid4()

# store this node transactions in a list
this_nodes_transactions = []

# Store the url data of every
# other node in the network
# so that we can communicate
# with them
peer_nodes = []

# initialize the chain and add the genesis block
genesis_block  = create_genesis_block()

my_simple_chain = Chain()

my_simple_chain.add_genesis_block(genesis_block)

def send_mined_block_to_other_nodes(mined_block):

  for node_url in peer_nodes:
    url_to_post = node_url + '/block'
    # Post this node block chain to the newly added peer
    res = requests.post(url_to_post,
                    json=mined_block.to_json())

    print ('response from peer node:{}'.format(res.text))

def proof_of_work(target_hash):
    nonce = 0

    while (1):

        block = Block(0, target_hash, nonce, date.datetime.now(), {
        'proof-of-work': None,
        'transactions': None
        }, '0')

        nonce += 1

        if(int(block.hash, 16) < int(target_hash, 16)):
            proof = block
            break

    return proof

@node.route('/peer', methods=['POST'])
def add_peer():
    if request.method == 'POST':
        # On each new post request, we extracts the transaction data
        new_peer = request.args.get("node_url")

        # now append the new transaction into our list
        peer_nodes.append(new_peer)

        url_to_post = new_peer + '/blocks'
        # Post this node block chain to the newly added peer
        res = requests.post(url_to_post,
                        json=my_simple_chain.to_json())

        print ('response from peer node:{}'.format(res.text))

        # Show the new transaction info on the debug console
        print('New peer node address')
        print('Peer Address: {}'.format(new_peer))
        print('Peer Address: {}'.format(url_to_post))

        return 'Peer was added successfully\n'

@node.route('/peers', methods=['GET'])
def get_peers():
    # return the current chain in JSON
    return json.dumps(peer_nodes)

@node.route('/trx', methods=['POST'])
def transaction():

    if request.method == 'POST':
        # On each new post request, we extracts the transaction data
        new_trx = request.get_json()

        # now append the new transaction into our list
        this_nodes_transactions.append(new_trx)

        # Show the new transaction info on the debug console
        print('New transaction')
        print('From: {}'.format(new_trx['from']))
        print('To: {}'.format(new_trx['to']))
        print('Amount: {}\n'.format(new_trx['amount']))

        return 'Transaction was submitted successfully\n'

@node.route('/blocks', methods=['GET'])
def get_blocks():
    # return the current chain in JSON
    return json.dumps(my_simple_chain.to_json())

# This method would only be called when this node joins the existing peer network
@node.route('/blocks', methods=['POST'])
def new_chain():
    if request.method == 'POST':
        tmp_simple_chain = Chain()
        # On each new post request, we extracts the transaction data
        existing_chain = request.get_json()

        tmp_simple_chain.load_chain_from_list(existing_chain)
        # accept the existing chain
        if(my_simple_chain.accept_existing_chain(tmp_simple_chain)):
            return 'Existing chain accepted\n'
        else:
            return 'Invalid chain!!!\n'

@node.route('/block', methods=['POST'])
def new_block():
    if request.method == 'POST':
        # On each new post request, we extracts the transaction data
        new_block = request.get_json()
        founded_block = my_simple_chain.find_block(new_block['previous_hash'])
        if (founded_block):
            print('Found previous_hash={}'.format(new_block['previous_hash']))

            # Now check proof of work before accepting this new block
            if(int(new_block['data']['proof-of-work'], 16) < int(new_block['target_hash'], 16)):
                print('Proof of work has been verified!!!')
                # Accept the block by adding into our block chain
                my_simple_chain.block_from_other_node(founded_block,
                                                    new_block['index'],
                                                    new_block['timestamp'],
                                                    new_block['target_hash'],
                                                    new_block['nonce'],
                                                    new_block['data'],
                                                    new_block['hash'])
                # validate the integrity of the chain
                if(my_simple_chain.is_valid()):
                    print('Chain validity has been verified')
                else:
                    print('Chain is broken!!!!')
            else:
                print('Invalid Proof of work, rejecting the new block!!!')

        else:
            print('Not Found!!! previous_hash={}'.format(new_block['previous_hash']))

        # Show the new transaction info on the debug console
        print('New block')
        print('new block: {}'.format(new_block))

        return 'New block received\n'


@node.route('/mine', methods=['GET'])
def mine():
    # Get last block in the chain
    last_block = my_simple_chain.get_last_block()

     # Find the proof of work for
     # the current block being mined
     # Note: The program will hang here until a new
     #       proof of work is found
    proof = proof_of_work(get_target(last_block))
     # Once we find a valid proof of work,
     # we know we can mine a block so
     # we reward the miner by adding a transaction

    this_nodes_transactions.append(
        { 'from': 'network', 'to': str(miner_address), 'amount': 1 }
    )

     # Now we can gather the data needed
     # to create the new block
    new_block_data = {
        "proof-of-work": proof.hash,
        "transactions": list(this_nodes_transactions)
    }

     # Empty transaction list
    this_nodes_transactions[:] = []

    nonce = proof.nonce
    target_hash = proof.target_hash

    # add mined Block
    last_mined_block = my_simple_chain.add_block(
                        last_block,
                        target_hash,
                        nonce,
                        new_block_data)

    send_mined_block_to_other_nodes(last_mined_block)

    # Let the client know we mined a block
    return json.dumps(last_mined_block.to_json()) + '\n'

if __name__ == '__main__':
    #node.run()
    flaskrun(node)

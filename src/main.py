import datetime as date

from block.block import Block
from chain.chain import Chain

def create_genesis_block():
    block = Block(0, date.datetime.now(), 'This is Genesis block', '0')
    return block

def main():
    # initialize the chain and add the genesis block
    genesis_block  = create_genesis_block()

    my_simple_chain = Chain()

    last_block = my_simple_chain.add_genesis_block(genesis_block)

    for i in range(1,10):
        last_block = my_simple_chain.add_block(last_block, 'This is block # '+str(i))

    my_simple_chain.print_chain_data()

    if(my_simple_chain.is_valid()):
        print('Hurray chain is valid...')
    else:
        print('Chain has been compromised!!!!')

if __name__ == '__main__':
    main()

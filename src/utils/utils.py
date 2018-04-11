import hashlib
import datetime as date
import random
import optparse
import ecdsa
import base58

from block.block import Block

def get_signing_key(private_hex_key):
    signing_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_hex_key),
                                               curve = ecdsa.SECP256k1)
    return signing_key

def get_verifying_public_key(private_hex_key, signing_key):
    verifying_key = signing_key.get_verifying_key()
    return verifying_key.to_string()

def create_bitcoin_compatible_address(private_hex_key,
                                      signing_key,
                                      verifying_public_key):

    msg = 'Hello world!'
    check_msg = 'Hello world!'
    signed_msg = signing_key.sign(msg.encode('ascii'))
    vk = ecdsa.VerifyingKey.from_string(verifying_public_key, curve=ecdsa.SECP256k1)
    #print("signed message " + signed_msg.hex())
    assert vk.verify(signed_msg, check_msg.encode('ascii'))

    #print("this is the vk: " + verifying_key.to_string().hex())

    public_key_in_bytes = bytes(vk.to_string())
    public_key = bytes.fromhex("04") + vk.to_string()

    #print ("this is the public key: " + public_key.hex())

    sha256_1 = hashlib.sha256(public_key)

    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(sha256_1.digest())

    hashed_public_key = bytes.fromhex("00") + ripemd160.digest()

    #print("this is the hashed public key: " + hashed_public_key.hex())

    checksum_full = hashlib.sha256(hashlib.sha256(hashed_public_key).digest()).digest()

    #print("this is my full checksum (32 bytes, I only need 4 bytes): " + checksum_full.hex())

    checksum = checksum_full[:4]

    #print ("this is the real check sum only 4 bytes long: " + checksum.hex())

    bin_addr = hashed_public_key + checksum

    #print("this is my bin_addr: " + bin_addr.hex())

    FINALE_BTC_ADDRESS = base58.b58encode(bin_addr)

    #print ("this is my bitcoin address! " + FINALE_BTC_ADDRESS)

    #decode address to extract the hashed_public_key
    decoded_hashed_pub_key = base58.b58decode_check(FINALE_BTC_ADDRESS)[1:].hex()
    #print("this is the decoded hashed public key: " + decoded_hashed_pub_key)
    sha256_2 = hashlib.sha256(public_key)

    ripemd160_a = hashlib.new("ripemd160")
    ripemd160_a.update(sha256_2.digest())

    hashed_agin_public_key = ripemd160_a.digest()
    #print("this is hashed again public key: " + hashed_agin_public_key.hex())

    vk = ecdsa.VerifyingKey.from_string(public_key_in_bytes, curve=ecdsa.SECP256k1)

    assert vk.verify(signed_msg, check_msg.encode('ascii'))

    return FINALE_BTC_ADDRESS

def create_genesis_block():
    m = hashlib.sha256()

    timestamp = date.datetime.now()
    m.update(str(timestamp).encode('ascii') +
            str(random.randint(0x008000, 0x7FFFFF)).encode('ascii'))
    target_hash = m.hexdigest()

    block = Block(0, target_hash, 0, date.datetime.now(), {
    'proof-of-work': None,
    'transactions': None
    }, '0')

    return block

def get_target(last_block):
    # get the index of this block
    index = last_block.index

    # Change the target to last block hash after every 5 coins are created
    if((index !=0) and (index % 5 == 0)):
        target_hash = last_block.hash
    else:
        # otherwie keep the last block target
        target_hash = last_block.target_hash

    return target_hash

def flaskrun(app, default_host="127.0.0.1",
                  default_port="5000"):
    """
    Takes a flask.Flask instance and runs it. Parses
    command-line flags to configure the app.
    """

    # Set up the command-line options
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help="Hostname of the Flask app " + \
                           "[default %s]" % default_host,
                      default=default_host)
    parser.add_option("-P", "--port",
                      help="Port for the Flask app " + \
                           "[default %s]" % default_port,
                      default=default_port)

    # Two options useful for debugging purposes, but
    # a bit dangerous so not exposed in the help message.
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)
    parser.add_option("-p", "--profile",
                      action="store_true", dest="profile",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    # If the user selects the profiling option, then we need
    # to do a little extra setup
    if options.profile:
        from werkzeug.contrib.profiler import ProfilerMiddleware

        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app,
                       restrictions=[30])
        options.debug = True

    print(options.host)
    print(options.port)

    app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )

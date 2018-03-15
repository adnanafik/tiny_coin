from hashlib import sha256
import datetime as date
import random
import optparse

from block.block import Block

def create_genesis_block():
    m = sha256()

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

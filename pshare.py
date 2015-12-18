#!/usr/bin/python

from socket import socket, AF_INET, SOCK_STREAM
from flask import Flask, request, send_from_directory
from sys import argv

PATH_DIV = '/'

# Output strings
ERR_NUM_ARGS = "Error: Please specify a file to share."
ERR_FILE_NOT_ACCESSIBLE = "Error: The file specified does not exist or is not readable."
ERR_ARG_LESS_THAN_ZERO = "Errpr: The maximum number of transfers specified must be at least 0."
ERR_ARG_NOT_A_NUM = "Error: The maximum number of transfers specified must be a number."
ERR_ARG_FORMAT = "Format: python3 pshare.py <file_path> [max_transfers]"
INIT_SHARE_MSG = "Your file is now accessible at thess URLs: "
BASE_URL = "http://"

app = Flask(__name__)
file_name = ""
file_dir = ""
max_downloads = 0

@app.route('/', methods=["GET"])
def err_path():
    return "Incorrect filename specified."

@app.route('/<path:filename>', methods=["GET"])
def serve_file(filename):
    '''Serves the file to be shared.'''

    return send_from_directory(file_dir, file_name)

def validate_args():
    '''Validates the correct number of arguments and whether they point to accessible files.'''

    if len(argv) != 2 and len(argv) != 3:
        print(ERR_NUM_ARGS)
        return False
    if not file_exists(argv[1]):
        print(ERR_FILE_NOT_ACCESSIBLE)
        return False
    if len(argv) == 3:
        try: 
            if int(argv[2]) < 0:
                print(ERR_ARG_LESS_THAN_ZERO)
                return False
        except ValueError:
            print(ERR_ARG_NOT_A_NUM)
            return False
    return True

def file_exists(path):
    '''Verifies that a file exists and is readable at the given path.'''
    try:
        f = open(path, "rb")
    except:
        return False
    
    f.close()
    return True

def get_free_port_num():
    '''Gets a free port number to listen on.'''
    
    sock = socket(AF_INET, SOCK_STREAM) 
    sock.bind(("localhost", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

def get_all_net_address():
    '''Gets all networking addresses that we are listening on.'''

    addresses = ["localhost", "127.0.0.1"]
    # TODO

    return addresses

if __name__ == "__main__":
    # Validate arguments
    if not validate_args():
        print(ERR_ARG_FORMAT)
        exit(-1)

    port = get_free_port_num()
    file_name = argv[1].split(PATH_DIV)[-1]
    file_dir = PATH_DIV.join(argv[1].split(PATH_DIV)[:-1])
    max_downloads = argv[2] if len(argv) == 3 else 1
    print(INIT_SHARE_MSG)

    for address in get_all_net_address():
        print(BASE_URL + address + ':' + str(port) + "/" + file_name)

    # Start Flask app
    app.run(port=port) 

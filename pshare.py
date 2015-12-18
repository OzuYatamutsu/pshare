from socket import socket, AF_INET, SOCK_STREAM
from flask import Flask, request, send_from_directory
from sys import argv

PATH_DIV = '/'

# Output strings
ERR_NUM_ARGS = "Error: Please specify a file to share."
ERR_FILE_NOT_ACCESSIBLE = "Error: The file specified does not exist or is not readable."
ERR_ARG_FORMAT = "Format: python3 pshare.py <file_path>"
INIT_SHARE_MSG = "Your file is now accessible at thess URLs: "
BASE_URL = "http://"

app = Flask(__name__)
file_path = ""
file_dir = ""

@app.route('/', methods=["GET"])
def err_path():
    return "Incorrect filename specified."

@app.route('/<path:filename>', methods=["GET"])
def serve_file(filename):
    '''Serves the file to be shared.'''

    return send_from_directory(file_dir, file_path)

def validate_args():
    '''Validates the correct number of arguments and whether they point to accessible files.'''

    if len(argv) != 2:
        print(ERR_NUM_ARGS)
        return False
    if not file_exists(argv[1]):
        print(ERR_FILE_NOT_ACCESSIBLE)
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

if __name__ == "__main__":
    # Validate arguments
    if not validate_args():
        print(ERR_ARG_FORMAT)
        exit(-1)

    port = get_free_port_num()
    file_path = argv[1]
    file_dir = PATH_DIV.join(file_path.split(PATH_DIV)[:-1])
    print(INIT_SHARE_MSG)

    # TODO: Detect local and public IP address
    print(BASE_URL + "localhost:" + str(port) + "/")

    # Start Flask app
    app.run(port=port) 

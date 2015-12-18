from socket import socket, AF_INET, SOCK_STREAM
from flask import Flask, request

# Output strings
INIT_SHARE_MSG = "Your file is now accessible at thess URLs: "
BASE_URL = "http://"

app = Flask(__name__)

app.route('/', "GET")
def serve_file():
    '''Serves the file to be shared.'''
    pass

def get_free_port_num():
    '''Gets a free port number to listen on.'''
    
    sock = socket(AF_INET, SOCK_STREAM) 
    sock.bind(("localhost", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

if __name__ == "__main__":
    # Start Flask app
    port = get_free_port_num()
    app.run(port=port)
    
    print(INIT_SHARE_MSG)
    # TODO: Detect local and public IP address
    print(BASE_URL + "localhost:" + port)

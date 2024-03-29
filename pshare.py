#!/usr/bin/python

from socket import socket, gethostname, gethostbyname_ex, AF_INET, SOCK_STREAM
from flask import Flask, request, send_from_directory
from psutil import net_connections
from sys import argv, version_info
from random import getrandbits
from threading import Timer
# Python 2/3 compatibility
if version_info >= (3, 0):
    from http.client import HTTPConnection
else:
    from httplib import HTTPConnection
from ipgetter2 import ipgetter1 as ipgetter
from requests import post
from os import path
# Output strings
ERR_NUM_ARGS = "Error: Please specify a file to share."
ERR_FILE_NOT_ACCESSIBLE = "Error: The file specified does not exist or is not readable."
ERR_ARG_LESS_THAN_ZERO = "Errpr: The maximum number of transfers specified must be at least 0."
ERR_ARG_NOT_A_NUM = "Error: The maximum number of transfers specified must be a number."
ERR_ARG_FORMAT = "Format: python3 pshare.py <file_path> [max_transfers]"
ERR_TOO_MANY_DOWNLOADS = "Error: Too many downloads. Ask your sharer to allow more!"
INFO_SHUTTING_DOWN = "Transfers complete! Shutting down server..."
INIT_SHARE_MSG = "Your file is now accessible at these URLs: "
BASE_URL = "http://"

app = Flask(__name__)
file_name = ""
file_dir = ""
num_downloads = 0
max_downloads = 0
client_table = []
kill_code = str(getrandbits(64))

@app.route('/', methods=["GET"])
def err_path():
    return "Incorrect filename specified."

@app.route('/<path:filename>', methods=["GET"])
def serve_file(filename):
    '''Serves the file to be shared.'''
   
    global client_table
    global num_downloads
    global max_downloads

    client = request.remote_addr
    if max_downloads > 0 and client not in client_table:
        if num_downloads + 1 > max_downloads:
            return ERR_TOO_MANY_DOWNLOADS
        client_table.append(client)
        num_downloads += 1
        # Trigger checking of client socket on timeout thread
        Timer(0.5, socket_poll, [client]).start()
    return send_from_directory(file_dir, file_name)

@app.route('/' + kill_code, methods=["POST"])
def shutdown_flask():
    '''Stops the Flask server.'''

    func = request.environ.get("werkzeug.server.shutdown")
    func()

def trigger_shutdown():
    '''Sends a GET with the generated kill_code to trigger a shutdown of Flask.'''

    global port
    global kill_code

    post("http://localhost:" + str(port) + "/" + kill_code)

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
    addresses.insert(1, gethostname())
    addresses += gethostbyname_ex(gethostname())[2]
    if have_internet():
        try:        
            public_ip = ipgetter.myip()
            if public_ip not in addresses: addresses.append(public_ip)
        except Exception:
            # Swallow it
            pass
    return addresses

def socket_poll(ip):
    '''Controls what happens if a client socket closes.'''

    global client_table
    if is_ip_still_there(ip):
        # Check again later
        Timer(0.5, socket_poll, [ip]).start()
        return
    client_table.remove(ip)
    if len(client_table) == 0 and num_downloads >= max_downloads:
        print(INFO_SHUTTING_DOWN)
        trigger_shutdown()

def is_ip_still_there(ip):
    '''Checks if we still have an open socket to a given ip address.'''

    netstat_filter_table = [
        sock for sock in net_connections() \
        if ip in sock.raddr \
        and port in sock.raddr \
    ]

    return len(netstat_filter_table) != 0

def have_internet():
    '''Checks if we have a connection to the internet.'''

    conn = HTTPConnection("www.google.com")
    try:
        conn.request("HEAD", "/")
        return True
    except:
        return False

if __name__ == "__main__":
    # Validate arguments
    if not validate_args():
        print(ERR_ARG_FORMAT)
        exit(-1)

    port = get_free_port_num()
    file_name = argv[1].split(path.sep)[-1]
    file_dir = path.sep.join(argv[1].split(path.sep)[:-1])
    max_downloads = int(argv[2]) if len(argv) == 3 else 1
    print(INIT_SHARE_MSG)

    for address in get_all_net_address():
        print(BASE_URL + address + ':' + str(port) + "/" + file_name)

    # Start Flask app
    app.run(host="0.0.0.0", port=port) 

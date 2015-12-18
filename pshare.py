from socket import socket, AF_INET, SOCK_STREAM

def get_free_port_num():
    '''Gets a free port number to listen on.'''
    
    sock = socket(AF_INET, SOCK_STREAM) 
    sock.bind(("localhost", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

if __name__ == "__main__":
    print(get_free_port_num())

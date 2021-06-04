import socket


'''
Socket for packet transmission through the TUN interface
'''

# Socket initialization
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('127.0.0.1', 65432))

sock.sendall(b'Hello World!')
data = sock.recv(1024)

print(f'Received {repr(data)}')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Local addr, local port
# sock.bind(('127.0.0.1', 65535))


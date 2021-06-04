import socket


'''
Socket for packet transmission through the TUN interface
'''

# # Socket initialization
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding the socket to the TUN device
sock.bind(('127.0.0.1', 65432))

sock.listen()
conn, addr = sock.accept()

print(f'{addr} has connected!')

while True:
    data = conn.recv(1024)
    if not data:
        break
    print(f'Received {repr(data)}')
    conn.sendall(data)

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # Local addr, local port
# sock.bind(('127.0.0.1', 65432))

# msg, addr = sock.recvfrom(65535)

# print(f'{addr[0]} has connected!')

# remote_address = addr[0]
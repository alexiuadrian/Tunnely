import socket

socket_object = socket.socket()
host_name = socket.gethostname()
ip_address = socket.gethostbyname(host_name)
port = 666

socket_object.connect(('192.168.0.105', port))  # Ip-ul server-ului
print((socket_object.recv(1024)).decode('utf-8'))   # Decodeaza mesajul transmis din biti in string
socket_object.close()
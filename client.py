import socket

socket_object = socket.socket()
host_name = socket.gethostname()
port = 666

socket_object.connect((host_name, port))
print((socket_object.recv(1024)).decode('utf-8'))
socket_object.close()
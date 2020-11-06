import socket

socket_object = socket.socket()
host_name = socket.gethostname()
ip_address = socket.gethostbyname(host_name)
port = 666

socket_object.connect(('192.168.0.105', 1234))  # Ip-ul server-ului
print((socket_object.recv(1024)).decode('utf-8'))   # Decodeaza mesajul transmis din biti in string folosind utf-8
socket_object.close()
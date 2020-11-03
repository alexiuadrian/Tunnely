import socket

socket_object = socket.socket()
host_name = socket.gethostname()

port = 666
socket_object.bind((host_name, port))

socket_object.listen(5)

while True:
    client, addr = socket_object.accept()
    print("Got connection from ", addr)
    message = "Connected!".encode('utf-8')
    client.send(message)
    client.close()
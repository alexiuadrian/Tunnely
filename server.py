import socket

socket_object = socket.socket()
host_name = socket.gethostname()
ip_address = socket.gethostbyname(host_name)

port = 666

socket_object.bind(('192.168.0.105', port)) # Ip-ul serverului luat din ifconfig

socket_object.listen(5) # Poate asculta maxim 5 conexiuni simultane

while True:
    client, addr = socket_object.accept()
    print(addr, " s-a conectat!")
    message = "Ati fost conectat cu succes!".encode('utf-8')    # Codeaza mesajul in biti pentru a putea fi transmis
    client.send(message)
    client.close()
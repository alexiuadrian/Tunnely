import socket
import threading 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 666

sock.bind(('192.168.43.164', port))

sock.listen(1)

connections = []

def handler(client, client_ad):
    while True:
        data = client.recv(1024)
        for connection in connections:
            connection.send(bytes(data))
        if not data:
            connections.remove(client)
            client.close()
            break

while True:
    client, client_ad = sock.accept()
    cThread = threading.Thread(target=handler, args=(client, client_ad))
    cThread.daemon = True
    cThread.start()
    connections.append(client)
    print(connections)
import socket, sys
from _thread import *

def start_proxy():
    socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host_name = socket.gethostname()
    # ip_address = socket.gethostbyname(host_name)

    port = 6969

    socket_object.bind(('192.168.0.105', port)) # Ip-ul serverului luat din ifconfig

    socket_object.listen(5) # Poate asculta maxim 5 conexiuni simultane

    while True:
        try:
            client, addr = socket_object.accept()
            data = (client.recv(16384)).decode('utf-8')
            # print(data)
            start_new_thread(connection_string, (client, data, addr))
        except KeyboardInterrupt:
            socket_object.close()
            sys.exit(1)

    socket_object.close()

def connection_string(client, data, addr):
    first_line = data.split('\n')[0]
    url = first_line.split(' ')[1]
    http_pos = url.find("://")

    if(http_pos == -1):
        temp = url
    else:
        temp = url[(http_pos + 3):]
    
    port_pos = temp.find(":")

    webserver_pos = temp.find("/")

    if(webserver_pos == -1):
        webserver_pos = len(temp)

    webserver = ""
    port = -1

    if(port_pos == -1 or webserver_pos < port_pos):
        port = 80
        webserver = temp[:webserver_pos]
    else:
        port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
        webserver = temp[:port_pos]

    

    proxy_server(webserver, port, client, addr, data)

def proxy_server(webserver, port, client, addr, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((webserver, port))
    s.send(data.encode('utf-8'))

    while(1):
        reply = s.recv(16384)
        if(len(reply) > 0):
            client.send(reply)
        else:
            break
    
    s.close()
    client.close()


start_proxy()
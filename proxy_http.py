import socket
import threading
import sys

def start_proxy_server():

    socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socket_object.bind(("192.168.43.164", 6969))     # The socket is given an ip address and a port - the ip address belongs to the server that the port runs on
    
    socket_object.listen(1)        # The maxim number of simultaneous connections that the socket can listen to

    while True:     # Infinite loop for incoming connections on this port
        client, ip_client = socket_object.accept()        # Accepts the incoming connection which returns the client as a socket object and its ip address
        data = str(client.recv(1024), "utf-8")      # Receives the data sent by the client (in byte form so decoding is needed to turn it into string)
        cThread = threading.Thread(target=process_data, args=(data, client, ip_client))        # Start a new Thread to process the incoming request
        cThread.daemon = True
        cThread.start()
    socket_object.close()    # The socket is being closed after the processing is done


def process_data(data, client, ip_client):
    first_line = data.split('\n')[0]      # The url sits on the first line of the request 
    url = first_line.split(' ')[1]        # and is the second 'word' on that line

    http_pos = url.find("://")       # Returns the position of the "://" from the url

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

    connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_socket.connect((webserver, port))
    connection_socket.sendall(bytes(data, "utf-8"))

    while True:
        reply = connection_socket.recv(1024)
        conn_thread = threading.Thread(target=send_back, args=(reply, connection_socket, client))
        conn_thread.daemon = True
        conn_thread.start()
        if(conn_thread == -1):
            break
        # reply = connection_socket.recv(2048)
        # if(len(reply) > 0):
        #     client.send(reply)
        # else:
        #     break
    
    connection_socket.close()
    client.close()

def send_back(reply, server, client):
    if(len(reply) > 0):
        client.send(reply)
    else:
        return -1

start_proxy_server()
import socket
import threading
import sys
from _thread import *

def start_proxy_server():

    socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socket_object.bind(("192.168.0.105", 6969))     # The socket is given an ip address and a port - the ip address belongs to the server that the port runs on
    
    socket_object.listen(15)        # The maxim number of simultaneous connections that the socket can listen to

    while True:     # Infinite loop for incoming connections on this port
        client, ip_client = socket_object.accept()        # Accepts the incoming connection which returns the client as a socket object and its ip address
        data = (client.recv(4096)).decode('utf-8')      # Receives the data sent by the client (in byte form so decoding is needed to turn it into string)
        start_new_thread(process_data, (data, client, ip_client))        # Start a new Thread to process the incoming request

    socket_object.close()    # The socket is being closed after the processing is done


def process_data(data, client, ip_client):
    print(data)
    address_line = data.split('\n')[0]      # The url sits on the first line of the request 
    url = address_line.split(' ')[1]        # and is the second 'word' on that line

    aux_web = url.find("://")       # Returns the position of the "://" from the url

    web_address = ""
    port = -1

    if(aux_web != -1):      # Extracts the web_address from the url
        web_address = url[(aux_web + 3):]
        print(web_address)
        aux_port = web_address.find(":")
        if(aux_port != -1):
            web_address = web_address[:aux_port]
            port = int(url[(aux_port + 1):])
        else:
            port = 80
            if(web_address[len(web_address) - 1] == '/'):
                web_address = web_address[:(len(web_address) - 1)]
    else:
        web_address = url
        aux_port = web_address.find(":")
        if(aux_port != -1):
            web_address = web_address[:aux_port]
            port = int(url[(aux_port + 1):])
        else:
            port = 80
            if(web_address[len(web_address) - 1] == '/'):
                web_address = web_address[:(len(web_address) - 1)]
        

    print(web_address, port)

    connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_socket.connect((web_address, port))
    connection_socket.send(data.encode('utf-8'))

    while True:
        reply = connection_socket.recv(4096)
        if(len(reply) > 0):
            client.send(reply)
        else:
            break
    
    connection_socket.close()
    client.close()

start_proxy_server()
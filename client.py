import pytun
import subprocess
import socket
import select
from pytun import IFF_TAP
import os
import struct
import fcntl    
import sys
from cryptography.fernet import Fernet


def read_key_from_file(path_to_key):
    f = open(path_to_key, "r")
    
    content = f.read()
    
    return str.encode(content)

# Command line arguments from the tunnely bash script
path_to_key = sys.argv[1]
local_ip = sys.argv[2]
local_port = int(sys.argv[3])
remote_ip = sys.argv[4]
remote_port = int(sys.argv[5])
    

key = read_key_from_file(path_to_key)
print(key)

'''
Socket for packet transmission through the TUN interface
'''

# Socket initialization
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Binding the socket to the local computer
sock.bind((local_ip, local_port))

# sock.connect((remote_ip, remote_port))
sock.sendto(b"Hello", (remote_ip, remote_port))

'''
Creating the TAP interface
'''

tap = pytun.TunTapDevice(flags=pytun.IFF_TAP)

tap.addr = '10.8.0.2'
tap.netmask = '255.255.255.0'
tap.mtu = 1500

# Starting the TAP interface
tap.up()

os.system('sudo route add default gw 10.8.0.1')

info_to_sock = None
info_to_tap = None
devices = [tap, sock]

while True:
    read, write, x = select.select(devices, devices, [])

    if tap in read:
        info_to_sock = tap.read(1500)
        #print("INFO TO SOCK 1 ", info_to_sock)
    
    if sock in read:        
        info_to_tap, ad = sock.recvfrom(remote_port)
        
        f = Fernet(key)
        decr_info_to_tap = f.decrypt(info_to_tap)
        
        #print("INFO TO TAP 1 ", decr_info_to_tap)
        info_to_tap = decr_info_to_tap
    
    if info_to_tap and tap in write:
        
        tap.write(info_to_tap)
        #print("INFO TO TAP 2 ", info_to_tap)
        info_to_tap = None
    
    if info_to_sock and sock in write:
        #print("INFO TO SOCK 2 ", info_to_sock)
        
        f = Fernet(key)
        
        encr_info_to_sock = f.encrypt(info_to_sock)
        info_to_sock = None
        
        sock.sendto(encr_info_to_sock, (remote_ip, remote_port))

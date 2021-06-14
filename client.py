import pytun
import subprocess
import socket
import select
from pytun import IFF_TAP
import os
import struct
import fcntl    
import sys

# Command line arguments from the tunnely bash script
path_to_key = sys.argv[1]
local_ip = sys.argv[2]
local_port = int(sys.argv[3])
remote_ip = sys.argv[4]
remote_port = int(sys.argv[5])

'''
Socket for packet transmission through the TUN interface
'''

# tun = pynetlinux.tap.Tap()
# tun.set_ip('10.8.0.2')
# tun.set_netmask(24)
# tun.up()

# Socket initialization
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((local_ip, local_port))

#sock.connect(('192.168.0.106', 65432))

# sock.sendto(b'Init message', ('192.168.0.106', 65432))
# sock.connect(('79.117.253.249', 65432))
# msg, addr = sock.recvfrom(65432)
# print(1)
# sock.sendall(b'Init')
# print(2)
# data = sock.recv(1024)
# print(3)
# print(f'Received {repr(data)}')

# subprocess.call(['sysctl', '-w', 'net.ipv4.ip_forward=1'])

tap = pytun.TunTapDevice(flags=pytun.IFF_TAP)

tap.addr = '10.8.0.2'
tap.netmask = '255.255.255.0'
tap.mtu = 1500

# # Starting the TUN interface
tap.up()

# print(f'The device {tun.name} is up!')

# Making the TUN device the default route of the packets
#os.system('sudo route add default gw 10.8.0.1')

# tun = os.open('/dev/net/tun', os.O_RDWR | os.O_NONBLOCK)
# ifr = struct.pack(b'16sH', b'tap0', 2 | 4096)
# fcntl.ioctl(tun, 0x400454ca, ifr)

'''
Socket for packet transmission through the TUN interface
'''

# Socket initialization
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Binding the socket to the TUN device
# sock.bind(('10.8.0.2', 65535))


# Making the TUN interface persistant so it can be active
# after the user closed the program
# tun.persist(True)

info_to_sock = None
info_to_tap = None
devices = [tap, sock]

while True:
    read, write, x = select.select(devices, devices, [])

    if tap in read:
        # info_to_sock = tun.read(tun.mtu)
        #info_to_sock = os.read(tun, 1500)
        info_to_sock = tap.read(1500)
        print(b"INFO TO SOCK 1", info_to_sock)
    
    if sock in read:
        # sock.listen()
        # info_to_tun, addr = sock.accept()
        #info_to_tun, addr = sock.recvfrom(65432)
        info_to_tap, ad = sock.recvfrom(65432)
        print(b"INFO TO TAP 1", info_to_tap)
    
    if info_to_tap and tap in write:
        # tun.write(info_to_tun)
        #os.write(tun, info_to_tun)
        tap.write(info_to_tap)
        info_to_tap = None
        print(b"INFO TO TAP 2", info_to_tap)
    
    if info_to_sock and sock in write:
        sock.sendto(info_to_sock, (remote_ip, remote_port))
        #sock.sendall(info_to_sock)
        print(b"INFO TO SOCK 2", info_to_sock)
        info_to_sock = None

# Stopping the TUN interface
# tun.down()
# print(f"The device {tun.name} is down!")

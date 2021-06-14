from os import sendfile
import pytun
import time
import socket
import subprocess
import select
from pytun import IFF_TAP
import os
import struct
import fcntl
import sys
#sys.path.append('pathto/site-packages/pynetlinux')
#import pynetlinux

path_to_key = sys.argv[1]
local_ip = sys.argv[2]
local_port = int(sys.argv[3])
remote_ip = sys.argv[4]
remote_port = int(sys.argv[5])

info_to_sock = None
info_to_tap = None

os.system('sudo sysctl -w net.ipv4.ip_forward=1')

os.system('sudo iptables -t nat -A POSTROUTING -j MASQUERADE')

#tun = pynetlinux.tap.Tap()
#tun.set_ip('10.8.0.1')
#tun.set_netmask(24)
#tun.up()

#subprocess.call(['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-j', 'MASQUERADE'])

# # Socket initialization
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Binding the socket to the TUN device
sock.bind((local_ip, local_port))

# msg, addr = sock.recvfrom(56789)

#sock.listen()
#conn, addr = sock.accept()

# print(f'{addr} has connected!')

# info_to_tun, addr = sock.recvfrom(56789)

# print(f'{addr[0]} has connected!')

#print(b"INFO TO TUN CONN " + info_to_tun)

# while True:
#     data = conn.recv(1024)
#     if not data:
#         break
#     print(f'Received {repr(data)}')
#     conn.sendall(data)

# subprocess.call(['sysctl', '-w', 'net.ipv4.ip_forward=1'])

tap = pytun.TunTapDevice(flags=IFF_TAP)

tap.addr = '10.8.0.1'
tap.netmask = '255.255.255.0'
tap.mtu = 1500

# Starting the TUN interface
tap.up()

#print(f"The device {tun.name} is up!")

# Making the TUN interface persistent so it can be active
# after the user closed the program
# tun.persist(True)
# print(f"The server's {tun.name} is up!")
# tun.down()

#tun = os.open('/dev/net/tun', os.O_RDWR | os.O_NONBLOCK)
#ifr = struct.pack(b'16sH', b'tap0', 2 | 4096)
#fcntl.ioctl(tun, 0x400454ca, ifr)

devices = [tap, sock]

while True:
    read, write, x = select.select(devices, devices, [])

    if tap in read:
        # info_to_sock = tun.read(tun.mtu)
        #info_to_sock = os.read(tun, 1500)
        info_to_sock = tap.read(1500)
        print("INFO TO SOCK 1 ", info_to_sock)
    
    if sock in read:
        # info_to_tun, addr = sock.listen()
        #info_to_tun, addr = sock.recvfrom(56789)
        # sock.listen()
        # info_to_tun, addr = sock.accept()
        info_to_tap, ad = sock.recvfrom(remote_port)
        print("INFO TO TAP 1 ", info_to_tap)
    
    if info_to_tap and tap in write:
        # tun.write(info_to_tun)
        #os.write(tun, info_to_tun)
        tap.write(info_to_tap)
        print("INFO TO TAP 2 ", info_to_tap)
        info_to_tap = None
    
    if info_to_sock and sock in write:
        #sock.sendto(info_to_sock, (addr[0], 56789))
        print("INFO TO SOCK 2 ", info_to_tap)
        sock.sendto(info_to_sock, (remote_ip, remote_port))
        info_to_sock = None



'''
THIS SHOULD BE RUN ONLY ON THE CLIENT
'''
# Making the TUN device the default route of the packets
# subprocess.call(['/sbin/ip', 'route', 'add', 'default', 'dev', 'TunnelyTUN0'])

# Reading from the TUN device
# buf = tun.read(tun.mtu)



# while True:
#     buf = tun.read(tun.mtu)
#     # tun.write(buf)
#     print(f'Continut buffer: {buf}')

# Writing to the TUN device
# tun.write(buf)

# Stopping the TUN interface
# tun.down()
# print(f"The device {tun.name} is down!")

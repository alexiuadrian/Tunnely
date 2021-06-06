import pytun
import subprocess
import socket
import select
from pytun import IFF_TAP
import os
import struct
import fcntl

'''
Socket for packet transmission through the TUN interface
'''

# Socket initialization
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('192.168.43.22', 56789))

#sock.connect(('192.168.0.106', 65432))

# sock.sendto(b'Init message', ('192.168.0.106', 65432))
sock.connect(('79.117.253.249', 65432))
# print(1)
# sock.sendall(b'Init')
# print(2)
# data = sock.recv(1024)
# print(3)
# print(f'Received {repr(data)}')

# subprocess.call(['sysctl', '-w', 'net.ipv4.ip_forward=1'])

# tun = pytun.TunTapDevice(flags=pytun.IFF_TAP)

# tun.addr = '10.8.0.2'
# # tun.dstaddr = '10.8.0.1'
# tun.netmask = '255.255.255.0'
# tun.mtu = 1500

# # Starting the TUN interface
# tun.up()

# print(f'The device {tun.name} is up!')

# Making the TUN device the default route of the packets
subprocess.call(['sudo', '/sbin/ip', 'route', 'add', 'default', 'gw', '10.8.0.1'])

tun = os.open('/dev/net/tun', os.O_RDWR | os.O_NONBLOCK)
ifr = struct.pack('16sH', 'tap0', 2 | 4096)
fcntl.ioctl(tun, 0x400454ca, ifr)

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
info_to_tun = None
devices = [tun, sock]

while True:
    read, write, x = select.select(devices, devices, [])

    if tun in read:
        info_to_sock = tun.read(tun.mtu)
        print(b"INFO TO SOCK 1" + info_to_sock)
    
    if sock in read:
        # sock.listen()
        # info_to_tun, addr = sock.accept()
        info_to_tun, addr = sock.recvfrom(65432)
        print(b"INFO TO TUN 1" + info_to_tun)
    
    if info_to_tun and tun in write:
        tun.write(info_to_tun)
        print(b"INFO TO TUN 2" + info_to_tun)
        info_to_tun = None
    
    if info_to_sock and sock in write:
        sock.sendto(info_to_sock, ('79.117.253.249', 65432))
        #sock.sendall(info_to_sock)
        print(b"INFO TO SOCK 2" + info_to_sock)
        info_to_sock = None

# Stopping the TUN interface
# tun.down()
# print(f"The device {tun.name} is down!")

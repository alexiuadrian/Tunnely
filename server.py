from os import sendfile
import pytun
import time
import socket
import subprocess
import select
from pytun import IFF_TAP

info_to_sock = None
info_to_tun = None

# # Socket initialization
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding the socket to the TUN device
sock.bind(('192.168.0.106', 65432))

sock.listen()
conn, addr = sock.accept()

# print(f'{addr} has connected!')

# info_to_tun, addr = sock.recvfrom(56789)

print(f'{addr[0]} has connected!')

#print(b"INFO TO TUN CONN " + info_to_tun)

# while True:
#     data = conn.recv(1024)
#     if not data:
#         break
#     print(f'Received {repr(data)}')
#     conn.sendall(data)

tun = pytun.TunTapDevice(flags=IFF_TAP)

tun.addr = '10.8.0.1'
tun.netmask = '255.255.255.0'
tun.mtu = 1500

# Starting the TUN interface
tun.up()

print(f"The device {tun.name} is up!")

# Making the TUN interface persistent so it can be active
# after the user closed the program
# tun.persist(True)
# print(f"The server's {tun.name} is up!")
# tun.down()

devices = [tun, sock]

while True:
    read, write, x = select.select(devices, devices, [])

    if tun in read:
        info_to_sock = tun.read(tun.mtu)
        # print(b"INFO TO SOCK 1 " + info_to_sock)
    
    if sock in read:
        # info_to_tun, addr = sock.listen()
        info_to_tun, addr = sock.recvfrom(56789)
        # sock.listen()
        # info_to_tun, addr = sock.accept()
        print(b"INFO TO TUN 1 " + info_to_tun)
    
    if info_to_tun and tun in write:
        tun.write(info_to_tun)
        print(b"INFO TO TUN 2 " + info_to_tun)
        info_to_tun = None
    
    if info_to_sock and sock in write:
        sock.sendto(info_to_sock, (addr[0], 56789))
        print(b"INFO TO SOCK 2 " + info_to_tun)
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
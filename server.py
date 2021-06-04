from os import sendfile
import pytun
import time
import socket
import subprocess
import select

# # Socket initialization
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding the socket to the TUN device
sock.bind(('192.168.0.106', 65432))

sock.listen()
conn, addr = sock.accept()

print(f'{addr[0]} has connected!')

while True:
    data = conn.recv(1024)
    if not data:
        break
    print(f'Received {repr(data)}')
    conn.sendall(data)

tun = pytun.TunTapDevice(name="TunnelyTUN0")

tun.addr = '10.8.0.1'
#tun.dstaddr = '10.8.0.1'
tun.netmask = '255.255.255.0'
tun.mtu = 1500

# Starting the TUN interface
tun.up()

# Making the TUN interface persistent so it can be active
# after the user closed the program
# tun.persist(True)
print(f"The server's {tun.name} is up!")

info_to_sock = None
info_to_tun = None
devices = [tun, sock]

while True:
    read, write, x = select.select(devices, devices, [])

    if tun in read:
        info_to_sock = tun.read(tun.mtu)
    
    if sock in read:
        info_to_tun, addr = sock.listen()
    
    if info_to_tun != None and tun in write:
        tun.write(info_to_tun)
        info_to_tun = None
    
    if info_to_sock != None and sock in write:
        sock.sendto(info_to_sock, ('192.168.0.103', 56789))
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
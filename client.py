import pytun
import subprocess
import socket

tun = pytun.TunTapDevice(name="TunnelyTUN1")

tun.addr = '10.8.0.2'
#tun.dstaddr = '10.8.0.1'
tun.netmask = '255.255.255.0'
tun.mtu = 1500

# Starting the TUN interface
tun.up()

# Making the TUN device the default route of the packets
subprocess.call(['/sbin/ip', 'route', 'add', 'default', 'dev', 'TunnelyTUN1'])


'''
Socket for packet transmission through the TUN interface
'''

# Socket initialization
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Binding the socket to the TUN device
sock.bind(('10.8.0.2', 65535))


# Making the TUN interface persistant so it can be active
# after the user closed the program
tun.persist(True)
print(f"The server's {tun.name} is up!")

# Stopping the TUN interface
tun.down()
print(f"The device {tun.name} is down!")
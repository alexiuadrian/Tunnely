import pytun
import time
import socket
import subprocess

tun = pytun.TunTapDevice(name="TunnelyTUN0")

tun.addr = '10.8.0.1'
#tun.dstaddr = '10.8.0.1'
tun.netmask = '255.255.255.0'
tun.mtu = 1500

# Starting the TUN interface
tun.up()

# Making the TUN interface persistent so it can be active
# after the user closed the program
tun.persist(True)
print(f"The server's {tun.name} is up!")


'''
THIS SHOULD BE RUN ONLY ON THE CLIENT
'''
# Making the TUN device the default route of the packets
# subprocess.call(['/sbin/ip', 'route', 'add', 'default', 'dev', 'TunnelyTUN0'])

# Reading from the TUN device
# buf = tun.read(tun.mtu)



# while True:
#     buf = tun.read(tun.mtu)
#     tun.write(buf)
#     print(len(buf))

# Writing to the TUN device
# tun.write(buf)

# Stopping the TUN interface
# tun.down()
# print(f"The device {tun.name} is down!")
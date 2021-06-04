from fcntl import ioctl
import os
import pytun
import struct
import string

descriptor = os.open('/dev/net/tun', os.O_RDWR | os.O_NONBLOCK)

ioctl(descriptor, 0x400454ca, struct.pack("16sH".encode('utf-8'), 'tap0'.encode('utf-8'), 0x0001 | 0x1000))
import os
import select
import socket
import sys
from cryptography.fernet import Fernet
import TunnelyCore as core



def start_tunnely(core_obj):
    # Maximum transmission units
    mtu = core_obj._mtu

    files = [core_obj._tap, core_obj._sock]
    to_tap = None
    to_sock = None
    tap = os.open("/dev/net/tun", os.O_RDWR | os.O_NONBLOCK)

    while True:
        r, w, aux = select.select(files, files, [])

        if core_obj._tap in r:
            to_sock = os.read(core_obj._tap, mtu)

        if core_obj._sock in r:
            to_tap, addr = core_obj._sock.recvfrom(65535)

            key = Fernet.generate_key()

            f = Fernet(key)

            decr_data = f.decrypt(to_tap)

            to_tap = decr_data

        if to_tap and core_obj._tap in w:
            core_obj._tap.write(to_tap)
            to_tap = None

        if to_sock and core_obj._sock in w:

            key = Fernet.generate_key()

            f = Fernet(key)

            encr_data = f.encrypt(to_sock)

            to_sock = encr_data

            core_obj._sock.sendto(to_sock, (core_obj._remote_address, core_obj._remote_port))

            to_sock = None

if sys.argv[1] == 's':
    server = core.Core(
        "10.0.0.1", "24", 32768,
        "0.0.0.0", 12000, "10.0.0.2",
        "1200")
    start_tunnely(server)
elif sys.argv[1] == 'c':
    client = core.Core(
        "10.0.0.2", "24", 32768,
        "0.0.0.0", 12000, "10.0.0.1",
        "1200")
    start_tunnely(client)

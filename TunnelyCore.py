import os
import select
import socket
import sys
import cryptography
import pynetlinux


class Core:

    def __init__(self, taddr, tmask, tmtu, laddr, lport, remote_address, remote_port):
        super(Core, self).__init__()
        self._tap = pynetlinux.tap.Tap()
        self._tap.set_ip(taddr)
        self._tap.set_netmask(int(tmask))
        self._tmtu = tmtu
        self._tap.up()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((laddr, lport))
        self._remote_address = remote_address
        self._remote_port = remote_port

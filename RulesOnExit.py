"""
This file is used when the VPN client has been closed
to remove the TAP device from the system thus enabling
normal connection and to remove the port forwarding
rule in order to avoid security holes
"""

import os


def set_rules():

    # Remove the TAP device
    os.system("sudo ip tuntap del tunnelytap0 mode tap")

    # Remove the port forwarding rule
    os.system("sudo echo 0 | sudo tee /proc/sys/net/ipv4/ip_forward")


set_rules()

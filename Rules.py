import os

# Change the rule for the current session only
os.system("echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward")
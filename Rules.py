import sys
import os


def set_rules(option):

    # Case for server side rules
    if option == "s":
        print(option)
        # Change the rule for the current session only
        os.system("sudo echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward")

        # Enables the MASQUERADE algorithm
        os.system("sudo iptables -t nat -A POSTROUTING -j MASQUERADE")

        # Creates a TAP device
        os.system("sudo ip tuntap add tunnelytap0 mode tap")

        # Assigns an address to the TAP device
        os.system("sudo ifconfig tunnelytap0 10.0.0.1/24")

        return True

    # Case for client side rules
    elif option == "c":

        # Creates a TAP device
        os.system("sudo ip tuntap add tunnelytap0 mode tap")

        # Assigns an address to the TAP device
        os.system("sudo ifconfig tunnelytap0 10.0.0.2/24")

        # Set TAP device as the default gateway
        os.system("sudo ip route change default via 10.0.0.2")

        return True

    else:
        print("Please choose 's' for server configuration or 'c' for client configuration")

        return False


if set_rules(sys.argv[1]):
    print("Rules have been successfully updated")
else:
    print("There was an error updating the rules. Please try again.")

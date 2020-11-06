import socket

# url = "https://www.gbmb.org/"

# http_pos = url.find("://")

# if(http_pos == -1):
#         temp = url
# else:
#     temp = url[(http_pos + 3):]

# print(temp)

# webserver_pos = temp.find("/")
# print(webserver_pos)

connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection_socket.connect(("google.com", 443))
# load additional Python modules
import socket
import time

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
ip_address = "192.168.0.100"#socket.gethostbyname(local_hostname)

print(ip_address)
# bind the socket to the port 23456, and connect
server_address = (ip_address, 23456)
sock.connect(server_address)
print("connecting to %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

import pickle
import struct

DataToSend = {"c": 0, "b": 0, "a": 0}

data = pickle.dumps(DataToSend, 0)
size = len(data)

# print("{}: {}".format(frame, size))
sock.sendall(struct.pack(">L", size) + data)

# close connection
sock.close()
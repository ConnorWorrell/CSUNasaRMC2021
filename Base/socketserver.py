# load additional Python module
import socket

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
ip_address = socket.gethostbyname(local_hostname)

# output hostname, domain name and IP address
print ("working on %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

# bind the socket to the port 23456
server_address = (ip_address, 23456)
print ('starting up on %s port %s' % server_address)
sock.bind(server_address)

# listen for incoming connections (server mode) with one connection at a time
sock.listen(1)

while True:
    # wait for a connection
    print ('waiting for a connection')
    connection, client_address = sock.accept()
    import struct
    payload_size = struct.calcsize(">L")


    try:
        # show who connected to us
        print ('connection from', client_address)

        data = b""
        # receive the data in small chunks and print it
        while True:
            while len(data) < payload_size:
                data += connection.recv(4096)
            if data:
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack(">L", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += connection.recv(4096)
                frame_data = data[:msg_size]
                data = data[msg_size:]

                import pickle
                import cv2

                frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                cv2.imshow('ImageWindow', frame)
                cv2.waitKey(1)

                # output received data
                print ("Data: %s" % data)
            else:
                # no more data -- quit the loop
                print ("no more data.")
                break
    finally:
        # Clean up the connection
        connection.close()
import socket
import time

DataToSend = None

# Starts a server and listens until a connection is made with the base
def InitilizeCommunication():
    # create TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # retrieve local hostname
    local_hostname = socket.gethostname()

    # get fully qualified hostname
    local_fqdn = socket.getfqdn()

    # get the according IP address
    ip_address = socket.gethostbyname(local_hostname)

    # output hostname, domain name and IP address
    print("working on %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

    # bind the socket to the port 23456
    server_address = (ip_address, 23456)
    print('starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # listen for incoming connections (server mode) with one connection at a time
    sock.listen(1)

    print('waiting for a connection')
    global connection
    connection, client_address = sock.accept()
    print("Connected to: " + str(client_address))

    global DataToSend
    DataToSend = None

import struct
import pickle
payload_size = struct.calcsize(">L") # Standard payload size, this must be the same across both base/robot/send/recieve

# Stalls process until data is recieved, returns structure
def CheckRecieveData():
    data = b""
    global connection

    while len(data) < payload_size: # Grab data until we have the payload size
        data += connection.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0] # get the size of the rest of the data

    while len(data) < msg_size: # Grab the rest of the data
        data += connection.recv(4096)
    CommunicationData = data[:msg_size]

    # Turn bytes back into structures
    CommunicationUpdate = pickle.loads(CommunicationData, fix_imports=True, encoding="bytes")

    return CommunicationUpdate

# Sends data to base
def SendData(DataToSend):

    data = pickle.dumps(DataToSend, 0) # Turns strucutres into bytes
    size = len(data)

    global connection
    connection.sendall(struct.pack(">L", size) + data)

# Function called as the process that handels the communication
def StartCommunication(sharedData,lock):
    InitilizeCommunication()
    while True:
        try: # if socket is open
            # Add data recieved to shared data of Data Recieved
            data = CheckRecieveData()
            for key in data.keys():
                lock.acquire()
                tmp = sharedData["DataRecieved"]
                if key not in tmp:
                    tmp[key] = []
                tmp[key] = tmp[key] + data[key]
                sharedData["DataRecieved"] = tmp
                sharedData["NewDataRecieved"] = True
                lock.release()

            time.sleep(sharedData["Ping"]) # Wait for ping time to elapse

            # Send data stored in data to send
            dataToSend = sharedData["DataToSend"]
            lock.acquire()
            sharedData["DataToSend"] = {}
            lock.release()
            SendData(dataToSend)

            # Update time, this is used to determine if we have lost connection somehow
            lock.acquire()
            sharedData["LastConnectTime"] = time.time()
            lock.release()
        except Exception as e: # socket is closed, wait for connection again
            print("connection closed",e)
            InitilizeCommunication()
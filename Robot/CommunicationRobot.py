# load additional Python modules
import socket

DataToSend = None

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
payload_size = struct.calcsize(">L")
def CheckRecieveData():
    data = b""
    global connection

    # tmp = connection.recv(4096)

    while len(data) < payload_size:
        data += connection.recv(4096)
        # print(data)
    # if data != previousdata:
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += connection.recv(4096)
    CommunicationData = data[:msg_size]
    # data = data[msg_size:]

    CommunicationUpdate = pickle.loads(CommunicationData, fix_imports=True, encoding="bytes")

    # output received data
    # print(CommunicationUpdate)
    # no more data -- quit the loop
    # print("no more data.")
    print("Recieved Data: " + str(CommunicationUpdate))
    return CommunicationUpdate

def SendData(DataToSend):
    print("Sending: " + str(DataToSend))

    data = pickle.dumps(DataToSend, 0)
    size = len(data)

    global connection
    connection.sendall(struct.pack(">L", size) + data)

import time
# import globals
def StartCommunication(sharedData):
    InitilizeCommunication()
    timelast = time.time()
    while True:
        # print(sharedData)
        # time.sleep(.5)
        data = CheckRecieveData()
        sharedData["DataRecieved"] = data
        sharedData["NewDataRecieved"] = True
        print("Data Recieved")
        time.sleep(0.5)
        SendData(sharedData["DataToSend"])
        sharedData["DataToSend"] = {}
        print("ping: " + str(time.time()-timelast))
        timelast=time.time()


# def ListenForData():
#     while True:
#         data = CheckRecieveData()
#         print("Data Recieved: " + str(data))
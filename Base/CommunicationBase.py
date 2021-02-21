import socket

def InitilizeCommunication (ip_address):
    if(ip_address == None or ip_address == "0"):
        ip_address = "192.168.0.100"

    # create TCP/IP socket
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # retrieve local hostname
    local_hostname = socket.gethostname()

    # get fully qualified hostname
    local_fqdn = socket.getfqdn()

    # get the according IP address
    # ip_address = "192.168.0.100"  # socket.gethostbyname(local_hostname)

    print(ip_address)
    # bind the socket to the port 23456, and connect
    server_address = (ip_address, 23456)

    sock.connect(server_address)
    print("connecting to %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))
    return [True,server_address]

import pickle
import struct
def SendData(DataToSend):
    print("Sending: " + str(DataToSend))
    data = pickle.dumps(DataToSend, 0)
    size = len(data)

    global sock
    sock.sendall(struct.pack(">L", size) + data)

payload_size = struct.calcsize(">L")
def CheckRecieveData():
    data = b""
    global sock
    while len(data) < payload_size:
        data += sock.recv(4096)
        # print(data)
    # if data != previousdata:
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += sock.recv(4096)
    CommunicationData = data[:msg_size]
    # data = data[msg_size:]

    CommunicationUpdate = pickle.loads(CommunicationData, fix_imports=True, encoding="bytes")

    # output received data
    # print(CommunicationUpdate)
    # no more data -- quit the loop
    # print("no more data.")
    print("Recieved Data: " + str(CommunicationUpdate))
    return CommunicationUpdate

import time
import globals
def ListenForData(SharedData,ip_address):
    InitilizeCommunication(ip_address)
    timelast = time.time()
    while True:
        SendData(SharedData["DataToSend"])
        SharedData["DataToSend"] = {}
        time.sleep(0.5)
        data = CheckRecieveData()
        SharedData["DataRecieved"] = data
        SharedData["NewDataRecieved"] = True
        print("Data Recieved: " + str(data))
        print("Ping: " + str(time.time()-timelast))
        timelast = time.time()


from multiprocessing import Process
import globals
def StartProcess(ip_address):
    print(ip_address)
    p = Process(target=ListenForData, args=(globals.sharedData,ip_address))
    p.start()
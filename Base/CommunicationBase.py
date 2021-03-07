import socket
import pickle
import struct
import time
from multiprocessing import Process
import globals

# Start communication as client
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

    # bind the socket to the port 23456, and connect
    server_address = (ip_address, 23456)

    sock.connect(server_address)
    print("connecting to %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))
    return [True,server_address]

# Sends data to robot in the form of [length of data, data1, data2, ..., data end]
def SendData(DataToSend):
    data = pickle.dumps(DataToSend, 0) # pickle changes structures into bytes
    size = len(data)

    global sock
    sock.sendall(struct.pack(">L", size) + data)

payload_size = struct.calcsize(">L") # Predetermined payload size, contains the number of bytes in the payload

# Stalls the process until data is recieved
def CheckRecieveData():
    data = b"" # empty bytes array
    global sock
    while len(data) < payload_size: # recieve payload size + beginning of message
        data += sock.recv(4096)
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]

    while len(data) < msg_size: # recieve the rest of the message
        data += sock.recv(4096)
    CommunicationData = data[:msg_size] # remove payload size from the bytes array

    # Reconstruct the strucutres using pickle
    CommunicationUpdate = pickle.loads(CommunicationData, fix_imports=True, encoding="bytes")

    return CommunicationUpdate

# Listens for data and sends back responce
# The main funciton executed to handel the communication between robot and base
def ListenForData(SharedData,lock,ip_address):
    [tmp,ip_address] = InitilizeCommunication(ip_address)
    SharedData["ConnectedAddress"] = ip_address

    while True:
        try: # Catches socket closes
            lock.acquire() # Lock thread during edits
            dataToSend = SharedData["DataToSend"] # duplicate data and finish edits
            SharedData["DataToSend"] = {}
            lock.release() # Unlock thread, edit complete
            SendData(dataToSend) # Send duplicated data

            time.sleep(SharedData["LocalPing"]) # Wait for ping time
            data = CheckRecieveData() # Stall until data is recieved
            if data != {}: # If we recieved some data, not just a ping: {}
                lock.acquire()
                SharedData["DataRecieved"] = data
                SharedData["NewDataRecieved"] = True
                lock.release()

            lock.acquire() # This is used to calculate ping time for the GUI
            SharedData["LastConnectTime"] = time.time()
            SharedData["ConnectionStatus"] = 0
            lock.release()

        except: # If the connection is closed somehow
            print("connection closed")
            reconnectionAttempts = 5
            Attempts = 0
            for i in range (reconnectionAttempts):
                SharedData["ConnectionStatus"] = 1 # Reconnecting
                Attempts = Attempts + 1
                try:
                    print("Attempting Reconnect: " + str(i+1))
                    sock.close()
                    [tmp, ip_address] = InitilizeCommunication("0") # TODO reconnection only works if server ip is 192.168.0.100
                    SharedData["ConnectedAddress"] = ip_address
                    break
                except Exception: # Unable to reconnect
                    pass
            if(Attempts == reconnectionAttempts):
                SharedData["ConnectionStatus"] = 2  # Disconnected
                print("Failed to reconnect, ending connection task")
                break

# Function called from GUI to start the communication process
def StartProcess(ip_address):
    print(ip_address)
    p = Process(target=ListenForData, args=(globals.sharedData,globals.ThreadLocker,ip_address))
    p.start()
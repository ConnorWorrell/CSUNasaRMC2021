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

# define example data to be sent to the server
# temperature_data = ["15", "22", "21", "26", "25", "19"]
# for entry in temperature_data:
#     print("data: %s" % entry)
#     new_data = str("temperature: %s\n" % entry).encode("utf-8")
#     sock.sendall(new_data)

    # wait for two seconds
    # time.sleep(2)

from cv2 import *
import pickle
import struct
# img ="QRCodeBoard.png"
# image = cv2.imread(img)

video = VideoCapture("QRCodeTracker/QRCodeTestVideo.avi")
framenum = 1
while(1):
    print("Sending Frame: " + str(framenum))
    x,image = video.read()

    result, frame = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

    data = pickle.dumps(frame, 0)
    size = len(data)


    # print("{}: {}".format(frame, size))
    startsend = time.time()
    sock.sendall(struct.pack(">L", size) + data)
    responce = sock.recv(1024)
    framenum = framenum + 1
    print(max(0,.0333-time.time()+startsend)[0][0])
    time.sleep(max(0,.0333-time.time()+startsend)[0][0])

    print("Recieved: ", responce)

# close connection
sock.close()
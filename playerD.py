import socket
import numpy
import time

UDP_IP = "127.0.0.1"
UDP_PORTA_SENT = 6454
UDP_PORTA_REC = 6453
bastao = False
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((UDP_IP, UDP_PORTA_REC))
while(True):
    if(bastao):
        msg = b"bastao"
        print("D passa bastao ---------------->")
        sock.sendto(msg, (UDP_IP, UDP_PORTA_SENT))
        bastao = False
        time.sleep(2)

    while True:
        data, addr = sock.recvfrom(100) # buffer size is 100 bytes
        if data == b"bastao":
            print("<----------------D recebeu o bastao")
            time.sleep(2)
            bastao = True
            break
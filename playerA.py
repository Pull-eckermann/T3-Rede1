import socket
import numpy
import time

UDP_IP = "127.0.0.1"
UDP_PORTA_SENT = 6451
UDP_PORTA_REC = 6454
bastao = True
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((UDP_IP, UDP_PORTA_REC))
while(True):
    if(bastao):
        msg = b"bastao"
        print("A passa bastao ---------------->")
        sock.sendto(msg, (UDP_IP, UDP_PORTA_SENT))
        bastao = False
        time.sleep(2)
    
    while True:
        data, addr = sock.recvfrom(100) # buffer size is 1024 bytes
        if data == b"bastao":
            print("<----------------A recebeu o bastao")
            time.sleep(2)
            bastao = True
            break

import socket

from playerA import UDP_PORTA_SENT

UDP_IP = "127.0.0.1"
UDP_PORTA_SENT = 6451

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
#Recebe
msg = "Hello World"
dest = (UDP_IP, UDP_PORTA_SENT)
sock.sendto(msg, dest)

#Envia
sock.bind((UDP_IP, UDP_PORT))

while True:
  data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
  print("received message: %s" % data)
  
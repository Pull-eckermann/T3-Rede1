import socket
import numpy
import struct
import comp_functions

#Cabeçalho de envio pela rede
UDP_IP = "127.0.0.1"
UDP_PORTA_REC = 6454
UDP_PORTA_SENT = 6451

#Globais
bastao = False
saldo = 5

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((UDP_IP, UDP_PORTA_REC))
print('***INICIO DO JOGO***')
while(True):
    #Você é a origem e possui o bastão -----------------------------------------
    if(bastao):
        print('Sua vez de apostar')
        #Colhe informaçẽos da jogada
        print("""Combinações possíveis:
                1-PAR
                2-TRI0
                3-PARES_2
                4-FULL_HOUSE
                5-SEQUENCIA_BAIXA
                6-SEQUENCIA_ALTA
                7-QUADRA
                8-QUINTETO

                """)
        aposta = (int) (input('Qual será a combinação escolhida?(Escolha um número de 1 a 8): '))
        print("Seu saldo:", saldo)
        valor = (int) (input('Valor da aposta (Valor mínimo 1 ficha): '))
        packed = struct.pack('c i i', b'B', aposta, valor) # em ordem: Holder, aposta, valor
        sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))
        
        #Aguarda a apostas encerrarem e encaminha aposta ao jogador
        data, _ = sock.recvfrom(1024) 
        upk = struct.unpack('c i i', data)  # em ordem: Holder, aposta, valor da aposta
        #---------------------------------------------------------------------------------------------
        #Origem é o Holder
        if(upk == b'B'):
            comb = comp_functions.combination(upk[1])
            print('Jogador B ira jogar apostando a combinação '+comb+' num valor de '+upk[2])
            #************Logica da jogada**************
            saldo = saldo - upk[2]
              #Finge que jogou e ganhou pra testes
              #FALTA IMPLEMENTAR LÓGICA DAS JOGADAS
            saldo = saldo + comp_functions.pontuation(upk[1])
            result = True
            #**************Fim da jogada***************
            if result == False: #Indica que a origem perdeu
                print('O jogador B perdeu a jogada')
                if saldo <= 0:
                    print('O jogador B atingiu saldo nulo')
                    print('***FIM DE JOGO***')
                    exit(0)
                else:
                    print('Seu saldo e de '+saldo+'fichas')
                                    # em ordem: origem, jogador, resultado, saldo
                    packed = struct.pack('c c i i', b'B', b'B', 0, saldo)
                    sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))

            if result == True: #Indica que o jogador venceu
                print('O jogador B venceu a jogada')
                print('Seu saldo e de '+saldo+'fichas')
                       # em ordem: origem, jogador, resultado, saldo
                packed = struct.pack('c c i i', b'B', b'B', 1, saldo)
                sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))
        #---------------------------------------------------------------------------------------------
        #Outro jogador tem a vez de jogar, informa a ele
        else:
            comb = comp_functions.combination(upk[1])
            print('Jogador '+upk[0]+' ira jogar apostando a combinação '+comb+' num valor de '+upk[2])
                                    # em ordem: origem, destino, combinação, valor
            packed = struct.pack('c c i i', b'B', upk[0], upk[1], upk[2])
            sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))   #Informa ao jogador que ele pode realizar a jogada

            #Aguarda mensagem da jogada encerrada
            while True:    
                data, _ = sock.recvfrom(1024)
                        # em ordem: Origem, destino, resultado, saldo
                upk = struct.unpack('c c i i', data)
                if upk[1] == b'B':
                    if upk[2] == 0: #Indica que o jogador perdeu
                        print('O jogador '+upk[0]+' perdeu a jogada')
                        if upk[3] <= 0:
                            print('O jogador '+upk[0]+' atingiu saldo nulo')
                            print('***FIM DE JOGO***')
                            exit(0)
                        else:
                            print('Seu saldo e de '+upk[3]+'fichas')
                                        # em ordem: origem, jogador, resultado, saldo
                            packed = struct.pack('c c i i', b'B', upk[1], upk[2], upk[3])
                            sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))
                            break

                if upk[2] == 1: #Indica que o jogador venceu
                    print('O jogador '+upk[0]+' venceu a jogada')
                    print('Seu saldo e de '+upk[3]+'fichas')
                            # em ordem: origem, jogador, resultado, saldo
                    packed = struct.pack('c c i i', b'B', upk[1], upk[2], upk[3])
                    sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))
                    break
        #---------------------------------------------------------------------------------------------
        #Aguarda menssagem dar a volta na rede, fim da partida e passa o bastão
        while True:    
            data, _ = sock.recvfrom(1024) # buffer size is 1024 bytes
            upk = struct.unpack('c c i i', data)
            if upk[0] == b'B':  #Mensagem passou por toda a rede
                print('Vez do jogador C')
                jogada = b'bastao'
                sock.sendto(jogada, (UDP_IP, UDP_PORTA_SENT))
                bastao = False
                pass        #Passa para o próximo laço
    
    else: #Você não possui o bastão -----------------------------------------
        pass

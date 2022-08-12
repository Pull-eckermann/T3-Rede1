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
        print("Saldo:", saldo)
        valor = (int) (input('Valor da aposta (Valor mínimo 1): '))
        packed = struct.pack('c i i', b'B', aposta, valor) # em ordem: Holder, aposta, valor
        sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))
        
        #Aguarda a apostas encerrarem e encaminha aposta ao jogador
        data, _ = sock.recvfrom(1024) # buffer size is 1024 bytes
        upk = struct.unpack('c i i', data)
        if(upk == b'D'):    #Origem é quem tem a vez de jogar
            pass
            #AQUI DEVE SER FEITO A LÓGICA DA JOGADA
            #SE A ORIGEM FOR QUEM DETEM A VEZ DE JOGAR


        comb = comp_functions.combination(upk[1])
        print('Jogador '+upk[0]+' ira jogar apostando a combinação'+comb+' num valor de '+upk[2])
                                # em ordem: origem, destino, combinação, valor
        packed = struct.pack('c c i i', b'D', upk[0], upk[1], upk[2])
        sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))   #Informa ao jogador que ele pode realizar a jogada

        #Aguarda mensagem da jogada encerrada
        while True:    
            data, _ = sock.recvfrom(1024)
                    # em ordem: Origem, destino, resultado, saldo
            upk = struct.unpack('c c i i', data)
            if upk[1] == b'D':
                if upk[2] == 0: #Indica que o jogador perdeu
                    print('O jogador '+upk[0]+' perdeu a jogada')
                    if upk[3] <= 0:
                        print('O jogador '+upk[0]+' atingiu saldo nulo')
                        print('***FIM DE JOGO***')
                        break
                    else:
                        print('Seu saldo e de '+upk[3]+'fichas')
                                    # em ordem: Origem,jogador, resultado, saldo
                        packed = struct.pack('c c i i', b'D', upk[1], upk[2], upk[3])
                        break

                if upk[2] == 1: #Indica que o jogador venceu
                    print('O jogador '+upk[0]+' venceu a jogada')
                    print('Seu saldo e de '+upk[3]+'fichas')
                            # em ordem: Origem, jogador, resultado, saldo
                    packed = struct.pack('c c i i', b'D', upk[1], upk[2], upk[3])
                    break
        
        #Informou o saldo a todos os jogadores, fim da partida e passa o bastão
        while True:    
            data, _ = sock.recvfrom(1024) # buffer size is 1024 bytes
            upk = struct.unpack('c c i i', data)
            if upk[0] == b'D':  #Mensagem passou por toda a rede
                print('Vez do jogador A')
                jogada = b'bastao'
                sock.sendto(jogada, (UDP_IP, UDP_PORTA_SENT))
                bastao = False
                pass        #Passa para o próximo laço
    
    else: #Você não possui o bastão -----------------------------------------
        pass
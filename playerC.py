import socket
import numpy
import struct
import comp_functions

#Cabeçalho de envio pela rede
UDP_IP = "127.0.0.1"
UDP_PORTA_REC = 6452
UDP_PORTA_SENT = 6453

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
        aposta = int(input('Qual será a combinação escolhida?(Escolha um número de 1 a 8): '))
        print("Seu saldo: ", saldo)
        valor = int(input('Valor da aposta (Valor mínimo 1 ficha): '))
        packed = struct.pack('c i i', b'C', aposta, valor) # em ordem: Holder, aposta, valor
        sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))
        print('Aguardando aposta...')

        #Aguarda a apostas encerrarem e encaminha aposta ao jogador
        data, _ = sock.recvfrom(1024) 
        upk = struct.unpack('c i i', data)  # em ordem: Holder, aposta, valor da aposta
        #---------------------------------------------------------------------------------------------
        #Origem é o Holder
        if(upk[0] == b'C'):
            comb = comp_functions.combination(upk[1])
            print('Jogador C ira jogar apostando a combinação '+comb+' num valor de '+upk[2])
            #************Logica da jogada**************
            saldo = saldo - upk[2]
              #Finge que jogou e ganhou pra testes
              #FALTA IMPLEMENTAR LÓGICA DAS JOGADAS
            saldo = saldo + comp_functions.pontuation(upk[1])
            result = True
            #**************Fim da jogada***************
            if result == False: #Indica que a origem perdeu
                print('O jogador C perdeu a jogada')
                if saldo <= 0:
                    print('O jogador C atingiu saldo nulo')
                    print('***FIM DE JOGO***')
                    exit(0)
                else:
                    print('Seu saldo e de ',saldo,' fichas')
                                    # em ordem: origem, jogador, resultado, saldo
                    packed = struct.pack('c c i i', b'C', b'C', 0, saldo)
                    sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))

            if result == True: #Indica que o jogador venceu
                print('O jogador C venceu a jogada')
                print('Seu saldo e de ',saldo,' fichas')
                       # em ordem: origem, jogador, resultado, saldo
                packed = struct.pack('c c i i', b'C', b'C', 1, saldo)
                sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))
        #---------------------------------------------------------------------------------------------
        #Outro jogador tem a vez de jogar, informa a ele
        else:
            comb = comp_functions.combination(upk[1])
            print('Jogador ',upk[0],' ira jogar apostando a combinação '+comb+' num valor de ',upk[2])
                                    # em ordem: origem, Holder, combinação, valor
            packed = struct.pack('c c i i', b'C', upk[0], upk[1], upk[2])
            sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))   #Informa ao jogador que ele pode realizar a jogada

            #Aguarda mensagem da jogada encerrada
            while True:    
                data, _ = sock.recvfrom(1024)
                        # em ordem: Origem, Holder, resultado, saldo
                upk = struct.unpack('c c i i', data)
                if upk[0] == b'C':
                    if upk[2] == 0: #Indica que o jogador perdeu
                        print('O jogador ',upk[1],' perdeu a jogada')
                        if upk[3] <= 0:
                            print('O jogador ',upk[1],' atingiu saldo nulo')
                            print('***FIM DE JOGO***')
                            exit(0)
                        else:
                            print('Seu saldo e de ',upk[3],' fichas')
                                        # em ordem: origem, jogador, resultado, saldo
                            packed = struct.pack('c c i i', b'C', upk[1], upk[2], upk[3])
                            sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))
                            break

                    if upk[2] == 1: #Indica que o jogador venceu
                        print('O jogador ',upk[1],' venceu a jogada')
                        print('Seu saldo e de ',upk[3],' fichas')
                                # em ordem: origem, jogador, resultado, saldo
                        packed = struct.pack('c c i i', b'C', upk[1], upk[2], upk[3])
                        sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))
                        break
        #---------------------------------------------------------------------------------------------
        #Aguarda menssagem dar a volta na rede, fim da partida e passa o bastão
        while True:    
            data, _ = sock.recvfrom(1024) # buffer size is 1024 bytes
            upk = struct.unpack('c c i i', data)
            if upk[0] == b'C':  #Mensagem passou por toda a rede
                print('Vez do jogador C')
                jogada = b'bastao'
                sock.sendto(jogada, (UDP_IP, UDP_PORTA_SENT))
                bastao = False
                pass        #Passa para o próximo laço
    
    #Você não possui o bastão -----------------------------------------
    else:
        print('Aguardando aposta...')
        data, _ = sock.recvfrom(1024)
        upk = struct.unpack('c i i', data)  # em ordem: Holder, aposta, valor da aposta
        print('O Holder atual é: Jogador ',upk[0])
        print('Combinação apostada: '+comp_functions.combination(upk[1]))
        print('Valor da aposta: ',upk[2])

        decisao = input('Voce deseja tomar a aposta e aumentar o seu valor?[y/n]')
        if decisao == 'n':
            packed = struct.pack('c i i', upk[0], upk[1], upk[2])
            sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))
        else:
            print('Valor da aposta aumentado em 1')
            valor = upk[2] + 1
            packed = struct.pack('c i i', b'C', upk[1], valor)
            sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))
            print('Aguardando resultado...')
        
        #Aguarda para saber se será o holder
        data, _ = sock.recvfrom(1024)
        upk = struct.unpack('c c i i', data)    # em ordem: origem, holder, combinação, valor

        if upk[1] == b'C': #Você é holder
            print('Voce e o holder, considere que ganhou por teste somente')
            saldo = saldo - upk[3]
              #Finge que jogou e ganhou pra testes
              #FALTA IMPLEMENTAR LÓGICA DAS JOGADAS
            saldo = saldo + comp_functions.pontuation(upk[2])
            result = True
            
            if result == False: 
                print('Voce perdeu a jogada')
                if saldo <= 0:
                    print('Voce atingiu saldo nulo')
                    print('***FIM DE JOGO***')
                    exit(0)
                else:
                    print('Seu saldo e de ',saldo,' fichas')
                                    # em ordem: origem, jogador, resultado, saldo
                    packed = struct.pack('c c i i', upk[0], b'C', 0, saldo)
                    sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))

            if result == True: #Indica que voce venceu
                print('Voce venceu a jogada')
                print('Seu saldo e de ',saldo,' fichas')
                       # em ordem: origem, jogador, resultado, saldo
                packed = struct.pack('c c i i', upk[0], b'C', 1, saldo)
                sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))

        else:   #Você não é o holder, passa a mensagem pra frente
            print('Voce nao e o Holder, aguarde o resultado das jogadas...')
            packed = struct.pack('c c i i', upk[0], upk[1], upk[2], upk[3])
            sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT)) 

        #Aguarde o resultado da partida
        data, _ = sock.recvfrom(1024)
        upk = struct.unpack('c c i i', data)    # em ordem: Origem, Holder, resultado, saldo
        if upk[1] != b'C':  #Se você é o holder ignore, se não imprime na tela
            if upk[2] == 1:
                print('O jogador ',upk[1],' venceu a partida, seu saldo atual e: ',upk[3])
                print('Iniciando uma nova partida...')
                packed = struct.pack('c c i i', upk[0], upk[1], upk[2], upk[3])
                sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))
            else:
                print('O jogador ',upk[1],' perdeu a partida, seu saldo atual e: ',upk[3])
                print('Iniciando uma nova partida...')
                packed = struct.pack('c c i i', upk[0], upk[1], upk[2], upk[3])
                sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))
        else:
            packed = struct.pack('c c i i', upk[0], upk[1], upk[2], upk[3])
            sock.sendto(packed, (UDP_IP, UDP_PORTA_SENT))

        if upk[0] == b'B':
            data, _ = sock.recvfrom(1024)
            if data == b'bastao':
                print('Voce recebeu o bastao')
                bastao = True

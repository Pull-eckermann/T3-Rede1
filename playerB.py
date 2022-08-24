import socket
import numpy
import struct
import comp_functions
from time import sleep
import os

#Cabeçalho de envio pela rede
UDP_IP = "127.0.0.1"
UDP_PORTA_REC = 6451
UDP_PORTA_SENT = 6452
dest = (UDP_IP, UDP_PORTA_SENT)

#Globais
bastao = False
saldo = 5

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((UDP_IP, UDP_PORTA_REC))
os.system('clear')
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
        print("Seu saldo:", saldo)
        valor = int(input('Valor da aposta (Valor mínimo 1 ficha): '))
        dados = ('B', 'B', aposta, valor)
        comp_functions.send(sock, dest, dados)
        print('Aguardando aposta...')
        
        #Aguarda a apostas encerrarem e encaminha aposta ao jogador
        upk = comp_functions.receiv(sock)
        #---------------------------------------------------------------------------------------------
        #Origem é o Holder
        if(upk[1] == 'B'):
            dados = ('B', 'B', upk[2], upk[3])   # em ordem: Origem, Holder, aposta, valor da aposta
            comp_functions.send(sock, dest, dados)   #Informa ao jogador que ele pode realizar a jogada
            #Aguarda a mensagem retornar e começa as jogadas
            upk = comp_functions.receiv(sock)

            comb = comp_functions.combination(upk[2])
            print('Voce e o Holder, apostando a combinação '+comb+' num valor de',upk[3])
            sleep(2)
            result = comp_functions.lanca_dados(comb)

            if result == False: #Indica que a origem perdeu
                saldo = saldo - upk[3]
                print('Voce perdeu a jogada!!')
                if saldo <= 0:
                    print('Voce atingiu saldo nulo!')
                    dados = ('B', 'B', 0, saldo)
                    comp_functions.send(sock, dest, dados)
                    print('***FIM DE JOGO***')
                    exit(0)
                else:
                    print('Seu saldo e de ',saldo,'fichas')
                                    # em ordem: origem, jogador, resultado, saldo
                    dados = ('B', 'B', 0, saldo)
                    comp_functions.send(sock, dest, dados)

            if result == True: #Indica que o jogador venceu
                saldo = saldo + comp_functions.pontuation(upk[2])
                print('Voce venceu a jogada!!')
                print('Seu saldo e de',saldo,'fichas!')
                       # em ordem: origem, jogador, resultado, saldo
                dados = ('B', 'B', 1, saldo)
                comp_functions.send(sock, dest, dados)
        #---------------------------------------------------------------------------------------------
        #Outro jogador tem a vez de jogar, informa a ele
        else:
            comb = comp_functions.combination(upk[2])
            print('Jogador '+upk[1]+' ira jogar apostando a combinação '+comb+' num valor de',upk[3])

            dados =  ('B', upk[1], upk[2], upk[3])   # em ordem: origem, Holder, combinação, valor
            comp_functions.send(sock, dest, dados)   #Informa ao jogador que ele pode realizar a jogada

            #Aguarda mensagem da jogada encerrada
            while True:    
                upk = comp_functions.receiv(sock)    # em ordem: Origem, Holder, resultado, saldo
                if upk[0] == 'B':
                    if upk[2] == 0: #Indica que o jogador perdeu
                        print('O jogador '+upk[1]+' perdeu a jogada!!')
                        if upk[3] <= 0:
                            print('O jogador '+upk[1]+' atingiu saldo nulo!')
                            dados =  ('B', upk[1], upk[2], upk[3])
                            comp_functions.send(sock, dest, dados)
                            print('***FIM DE JOGO***')
                            exit(0)
                        else:
                            print('Seu saldo e de',upk[3],'fichas!')
                                        # em ordem: origem, Holder, resultado, saldo
                            dados =  ('B', upk[1], upk[2], upk[3])
                            comp_functions.send(sock, dest, dados)
                            break

                    if upk[2] == 1: #Indica que o jogador venceu
                        print('O jogador '+upk[1]+' venceu a jogada!!')
                        print('Seu saldo e de',upk[3],'fichas!')
                                # em ordem: origem, Holder, resultado, saldo
                        dados = ('B', upk[1], upk[2], upk[3])
                        comp_functions.send(sock, dest, dados)
                        break
        #---------------------------------------------------------------------------------------------
        #Aguarda menssagem dar a volta na rede, fim da rodada e passa o bastão
        while True:    
            upk = comp_functions.receiv(sock)
            if upk[0] == 'B':  #Mensagem passou por toda a rede
                print('Vez do jogador C!')
                jogada = b'bastao'
                sock.sendto(jogada, dest)
                bastao = False
                break        #Passa para o próximo laço
        print('************Iniciando uma nova rodada*************')
    #Você não possui o bastão -----------------------------------------
    else:
        print('Aguardando aposta...')
        upk = comp_functions.receiv(sock)  # em ordem: Origem, Holder, aposta, valor da aposta
        print('O Holder atual é: Jogador'+upk[1])
        print('Combinação apostada: '+comp_functions.combination(upk[2]))
        print('Valor da aposta:',upk[3])
        decisao = input('Voce deseja tomar a aposta e aumentar o seu valor?[y/n]')
        if decisao == 'n':
            dados = (upk[0], upk[1], upk[2], upk[3])
            comp_functions.send(sock, dest, dados)
            print('Aguardando resultado...')
        else:
            print('Valor da aposta aumentado em 1!')
            valor = upk[3] + 1
            dados = (upk[0], 'B', upk[2], valor)
            comp_functions.send(sock, dest, dados)
            print('Aguardando resultado...')
        
        #Aguarda para saber se será o holder
        upk = comp_functions.receiv(sock)    # em ordem: origem, holder, combinação, valor

        if upk[1] == 'B': #Você é holder
            comb = comp_functions.combination(upk[2])
            print('Voce e o Holder, apostando a combinação '+comb+' num valor de',upk[3])
            sleep(2)
            result = comp_functions.lanca_dados(comb)

            if result == False: #Indica que você perdeu
                saldo = saldo - upk[3]
                print('Voce perdeu a jogada!!')
                if saldo <= 0:
                    print('Voce atingiu saldo nulo!!')
                    dados = (upk[0], upk[1], 0, saldo)
                    comp_functions.send(sock, dest, dados)
                else:
                    print('Seu saldo e de',saldo,'fichas!!')
                                    # em ordem: origem, jogador, resultado, saldo
                    dados = (upk[0], upk[1], 0, saldo)
                    comp_functions.send(sock, dest, dados)

            if result == True: #Indica que o jogador venceu
                saldo = saldo + comp_functions.pontuation(upk[2])
                print('Voce venceu a jogada!!')
                print('Seu saldo e de',saldo,'fichas!')
                       # em ordem: origem, jogador, resultado, saldo
                dados = (upk[0], upk[1], 1, saldo)
                comp_functions.send(sock, dest, dados)

        else:   #Você não é o holder, passa a mensagem pra frente
            print('O Holder e '+upk[1]+', aguarde o resultado das jogadas...')
            dados = (upk[0], upk[1], upk[2], upk[3])
            comp_functions.send(sock, dest, dados) 

        #Aguarde o resultado da rodada
        upk = comp_functions.receiv(sock)    # em ordem: Origem, Holder, resultado, saldo
        if upk[1] != 'B':  #Se você é o holder ignore, se não imprime na tela
            if upk[2] == 1:
                print('O jogador '+upk[1]+' venceu a rodada! Seu saldo atual e:',upk[3])
                print('************Iniciando uma nova rodada*************')
                dados = (upk[0], upk[1], upk[2], upk[3])
                comp_functions.send(sock, dest, dados)
            else:
                print('O jogador '+upk[1]+' perdeu a rodada! Seu saldo atual e:',upk[3])
                dados = (upk[0], upk[1], upk[2], upk[3])
                comp_functions.send(sock, dest, dados)
                if upk[3] <= 0:
                    print('***FIM DE JOGO***')
                    exit(0)
                else:
                    print('************Iniciando uma nova rodada*************')
        else:
            dados = (upk[0], upk[1], upk[2], upk[3])
            comp_functions.send(sock, dest, dados)
            if saldo <= 0:
                print('***FIM DE JOGO***')
                exit(0)
            else:
                print('************Iniciando uma nova rodada*************')

        #Se a origem é de quem você recebe, aguarde o bastão
        if upk[0] == 'A':
            data, _ = sock.recvfrom(100)
            if data == b'bastao':
                print('Voce recebeu o bastao!!')
                bastao = True
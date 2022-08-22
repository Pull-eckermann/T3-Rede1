import re
import numpy
import random
import struct

#Tabela de pontuação
PAR = 1
TRI0 = 2
PARES_2 = 3
FULL_HOUSE = 4
SEQUENCIA_BAIXA = 5
SEQUENCIA_ALTA = 6
QUADRA = 8
QUINTETO = 10

def pontuation(indice):
  if indice == 1:
    return int(PAR)
  if indice == 2:
    return int(TRI0)
  if indice == 3:
    return int(PARES_2)
  if indice == 4:
    return int(FULL_HOUSE)
  if indice == 5:
    return int(SEQUENCIA_BAIXA)
  if indice == 6:
    return int(SEQUENCIA_ALTA)
  if indice == 7:
    return int(QUADRA)
  if indice == 8:
    return int(QUINTETO)

def combination(indice):
  if indice == 1:
    return 'par'
  if indice == 2:
    return 'trio'
  if indice == 3:
    return '2 pares'
  if indice == 4:
    return 'full house'
  if indice == 5:
    return 'sequencia baixa'
  if indice == 6:
    return 'sequencia alta'
  if indice == 7:
    return 'quadra'
  if indice == 8:
    return 'quinteto'

def lanca_dados(aposta):
  dado1 = dado2 = dado3 = dado4 = dado5 = 0
  d1 = d2 = d3 = d4 = d5 = False

  #Faz as jogadas de dados
  print('INICIANDO JOGADA DE DADOS')
  for i in range(1,4):
    print('-----------------------')
    print('Tentativa numero',i)
    if d1 == False:
      dado1 = random.randint(1, 6)
    print('Dado1:',dado1)
    if d2 == False:
      dado2 = random.randint(1, 6)
    print('Dado2:',dado2)
    if d3 == False:
      dado3 = random.randint(1, 6)
    print('Dado3:',dado3)
    if d4 == False:
      dado4 = random.randint(1, 6)
    print('Dado4:',dado4)
    if d5 == False:
      dado5 = random.randint(1, 6)
    print('Dado5:',dado5)
    if i != 3:
      print('Voce poder bloquear ate 5 dados')
      print('Digite, separando por espaço os dados que deseja bloquear (Ex\: 1 2 5)')
      k = input('(Se nenhum, digite 0): ')
      if k != '0':
        if '1' in k and d1 == False:
          d1 = True
        if '2' in k and d2 == False:
          d2 = True
        if '3' in k and d3 == False:
          d3 = True
        if '4' in k and d4 == False:
          d4 = True
        if '5' in k and d5 == False:
          d5 = True

  #avalia os resultados
  comb = 'Nenhum resultado'
  results = list([dado1, dado2, dado3, dado4, dado5])
  results.sort()
  #Se tem 2 ou 3 ou 4 ou 5 é sequencia
  if (2 in results) and (3 in results) and (4 in results) and (5 in results):
    if 1 in results:
      comb = combination(5) #Sequencia Baixa
    elif 6 in results:
      comb = combination(6) #Sequecia Alta
    else:
      comb = combination(1) #Par
  else: 
    aux = list()
    for i in range(1,7):
      if i in results:
        aux.append(i)
    if len(aux) == 4:
      comb = combination(1) #Par
    if len(aux) == 3:
      #Se algum dos elementos de aux for repetida 3 vezes, então é um trio
      if (results.count(aux[0]) == 3) or (results.count(aux[1]) == 3) or (results.count(aux[2]) == 3): 
        comb = combination(2) #Trio
      else:
        comb = combination(3) #Dois pares
    if len(aux) == 2:    
      if (results.count(aux[0]) == 3) or (results.count(aux[1]) == 3):
        comb = combination(4) #Full House
      else:
        comb = combination(7) #Full House
    if len(aux) == 1: 
        comb = combination(8) #Quinteto
  #Encerra a jogada
  print('Resultado da jogada: '+comb)
  if comb == aposta:
    return True
  else:
    return False
  
def send(sock, dest, dados):
  enquadramento = b'K'
  #Calcula CRC
  crc = dados[2]^dados[3]
  # em ordem: Enquadramento, Origem, Holder, aposta, valor, CRC
  packed = struct.pack('c c c i i i',enquadramento, dados[0].encode(), dados[1].encode(), dados[2], dados[3], crc)
  sock.sendto(packed, dest)

def receiv(sock):
  while True:
    data, _ = sock.recvfrom(100)
    # em ordem: Enquadramento, Origem, Holder, aposta, valor, CRC
    upk = struct.unpack('c c c i i i', data)
    if upk[0] == b'K':  #O enquadramento esta correto
      if upk[3]^upk[4] == upk[5]: #Não foi encontrado erro na mensagem
        dados = (upk[1].decode("utf-8"), upk[2].decode("utf-8"), upk[3], upk[4])
        return dados
      else:
        print('Erro: Mensagem apresenta modificacao no campo de dados')
        exit(0)

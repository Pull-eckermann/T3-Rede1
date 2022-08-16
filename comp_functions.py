from locale import DAY_6
import re
from sre_constants import JUMP
import numpy
import random

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
  dado1, dado2, dado3, dado4, dado5, dado6 = 0
  d1, d2, d3, d4, d5, d6 = False
  cont = 0

  #Faz as jogadas de dados
  print('INICIANDO JOGADA DE DADOS')
  for i in range(1,4):
    print('Tentativa numero',i)
    print('-----------------------')
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
    if d6 == False:  
      dado6 = random.randint(1, 6)
    print('Dado6:',dado6)
    print('-----------------------')
    print('Voce poder bloquear ate 5 dados')
    print('Digite, separando por espaço os dados que deseja bloquear(Se nenhum, digite 0)')
    k = input('Ex\: 1 2 5')
    if k != '0' or cont <= 5:
      if '1' in k and d1 == False:
        cont += 1
        d1 = True
      if '2' in k and d2 == False:
        cont += 1
        d2 = True
      if '3' in k and d3 == False:
        cont += 1
        d3 = True
      if '4' in k and d4 == False:
        cont += 1
        d4 = True
      if '5' in k and d5 == False:
        cont += 1
        d5 = True
      if '6' in k and d6 == False:
        cont += 1
        d6 = True
  
  #avalia os resultados
  results = list([dado1, dado2, dado3, dado4, dado5, dado6])
  




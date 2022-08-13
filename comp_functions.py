import numpy

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
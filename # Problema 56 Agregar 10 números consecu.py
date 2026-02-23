# Problema 56 Agregar 10 números consecutivos

lista_GR86 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

ultimo_RS = lista_GR86[-1]

for incremento_GT in range(1, 11):
    nuevo_valor_ZL1 = ultimo_RS + incremento_GT
    lista_GR86.append(nuevo_valor_ZL1)

print("Lista final:", lista_GR86)
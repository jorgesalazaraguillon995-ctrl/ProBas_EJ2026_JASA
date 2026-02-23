# Problema 53 Ordenar lista hasta que el usuario diga no

lista_RS = []

while True:
    modelo_GR = input("Ingrese dato: ")
    lista_RS.append(modelo_GR)
    
    continuar_GT = input("¿Desea continuar? (si/no): ")
    
    if continuar_GT.lower() != "si":
        break

lista_RS.sort()

print("Lista ordenada:")
print(lista_RS)
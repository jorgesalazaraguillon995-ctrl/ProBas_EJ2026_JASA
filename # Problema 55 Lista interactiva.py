# Problema 55 Lista interactiva

tipo_GT = input("¿Lista de números o texto? ")
lista_E36 = []

while True:
    
    print("\n1. Agregar")
    print("2. Eliminar por índice")
    print("3. Ordenar")
    print("4. Salir")
    
    opcion_RS = input("Elige opción: ")
    
    if opcion_RS == "1":
        valor_GR86 = input("Valor a agregar: ")
        
        if tipo_GT == "números":
            valor_GR86 = float(valor_GR86)
        
        lista_E36.append(valor_GR86)
    
    elif opcion_RS == "2":
        indice_ZL1 = int(input("Índice: "))
        lista_E36.pop(indice_ZL1)
    
    elif opcion_RS == "3":
        lista_E36.sort()
        print("Lista ordenada:", lista_E36)
    
    elif opcion_RS == "4":
        break
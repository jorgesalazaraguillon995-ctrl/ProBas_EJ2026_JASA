# Problema 50 Búsqueda por diferentes criterios

modo_busqueda_GT = input("Buscar por indice / modelo / clave: ")

if modo_busqueda_GT == "indice":
    i_RS = int(input("Índice: "))
    print(nombres_GT[i_RS], claves_RS[i_RS], stock_E36[i_RS])

elif modo_busqueda_GT == "modelo":
    nombre_E36 = input("Modelo: ")
    if nombre_E36 in nombres_GT:
        posicion_R34 = nombres_GT.index(nombre_E36)
        print(nombres_GT[posicion_R34], claves_RS[posicion_R34], stock_E36[posicion_R34])

elif modo_busqueda_GT == "clave":
    clave_GR = input("Clave: ")
    if clave_GR in claves_RS:
        posicion_ZL1 = claves_RS.index(clave_GR)
        print(nombres_GT[posicion_ZL1], claves_RS[posicion_ZL1], stock_E36[posicion_ZL1])
# Problema 54 Lista de ahorradores

nombres_ZL1 = []
ahorros_GT3 = []

cantidad_E36 = int(input("¿Cuántas personas? "))

for registro_R34 in range(cantidad_E36):
    nombre_GR86 = input("Nombre: ")
    ahorro_RS = float(input("Ahorro actual: "))
    
    nombres_ZL1.append(nombre_GR86)
    ahorros_GT3.append(ahorro_RS)

for revision_GT in range(cantidad_E36):
    if ahorros_GT3[revision_GT] < 1000:
        print(nombres_ZL1[revision_GT], "no tendrás para tu futuro")
    elif ahorros_GT3[revision_GT] > 1000000:
        print(nombres_ZL1[revision_GT], "ya casi te retiras")
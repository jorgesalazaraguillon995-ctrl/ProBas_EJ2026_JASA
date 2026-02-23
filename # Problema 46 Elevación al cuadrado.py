# Problema 46 Elevación al cuadrado

lista_GT = []

print("Registro de versiones especiales")

for pit_stop in range(10):
    potencia_base = float(input(f"Ingrese valor para versión {pit_stop+1}: "))
    lista_GT.append(potencia_base)

print("\nPotencias al cuadrado:")
for modo_ZL1 in lista_GT:
    potencia_stage2 = modo_ZL1 ** 2
    print(potencia_stage2)
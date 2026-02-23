# Problema 51 Registro de asistencia

trabajadores_GT = []
asistencia_RS = []

cantidad_E36 = int(input("¿Cuántos trabajadores? "))

for vuelta_GR86 in range(cantidad_E36):
    nombre_R34 = input("Nombre del trabajador: ")
    trabajadores_GT.append(nombre_R34)
    
    estado_ZL1 = int(input("Asistió (1 sí / 0 no): "))
    asistencia_RS.append(estado_ZL1)

for revision_GT3 in range(cantidad_E36):
    if asistencia_RS[revision_GT3] == 1:
        print(trabajadores_GT[revision_GT3], "sí asistió al turno")
    else:
        print(trabajadores_GT[revision_GT3], "no asistió al turno")
# Problema 47 Promedio por materia

total_materias_RS = int(input("¿Cuántas materias vas a registrar? "))

contador_E36 = 0

while contador_E36 < total_materias_RS:
    
    nombre_materia_GR86 = input("\nNombre de la materia: ")
    cantidad_notas_R34 = int(input("¿Cuántas calificaciones tiene esta materia? "))
    
    contador_notas_GT = 0
    acumulador_ZL1 = 0
    
    while contador_notas_GT < cantidad_notas_R34:
        nota_actual_RS = float(input(f"Calificación #{contador_notas_GT+1}: "))
        acumulador_ZL1 = acumulador_ZL1 + nota_actual_RS
        contador_notas_GT = contador_notas_GT + 1
    
    if cantidad_notas_R34 > 0:
        promedio_final_GT3 = acumulador_ZL1 / cantidad_notas_R34
    else:
        promedio_final_GT3 = 0
    
    print("=================================")
    print("Materia:", nombre_materia_GR86)
    print("Promedio final:", promedio_final_GT3)
    print("=================================")
    
    contador_E36 = contador_E36 + 1
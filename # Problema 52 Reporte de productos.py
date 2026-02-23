# Problema 52 Reporte de productos

productos_GT = []
precios_RS = []
ventas_R34 = []

contador_E36 = 0

while contador_E36 < 5:
    
    nombre_producto_GR86 = input("Producto: ")
    precio_producto_ZL1 = float(input("Precio: "))
    ventas_producto_GT3 = int(input("Unidades vendidas: "))
    
    productos_GT.append(nombre_producto_GR86)
    precios_RS.append(precio_producto_ZL1)
    ventas_R34.append(ventas_producto_GT3)
    
    contador_E36 = contador_E36 + 1

print("\n===== REPORTE GENERAL =====")

indice_RS = 0

while indice_RS < 5:
    
    ingreso_total_ZL1 = precios_RS[indice_RS] * ventas_R34[indice_RS]
    
    print("--------------------------------")
    print("Producto:", productos_GT[indice_RS])
    print("Precio:", precios_RS[indice_RS])
    print("Ventas:", ventas_R34[indice_RS])
    print("Ingreso total:", ingreso_total_ZL1)
    print("--------------------------------")
    
    indice_RS = indice_RS + 1
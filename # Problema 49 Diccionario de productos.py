# Problema 49 Diccionario de productos

garage_R34 = {}

for modo_GT in range(len(nombres_GT)):
    garage_R34[nombres_GT[modo_GT]] = {
        "clave": claves_RS[modo_GT],
        "stock": stock_E36[modo_GT]
    }

print("\nInventario general:")
print(garage_R34)
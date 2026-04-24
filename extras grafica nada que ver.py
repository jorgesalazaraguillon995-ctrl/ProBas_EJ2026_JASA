import matplotlib.pyplot as plt
import numpy as np

# Sabores de pays
x = np.array(["Limón", "Fresa", "Mango", "Queso"])

# Ventas o cantidad (ejemplo)
y = np.array([15, 10, 7, 12])

plt.bar(x, y)

# Títulos para que se vea más pro
plt.title("Ventas de Pays")
plt.xlabel("Sabores")
plt.ylabel("Cantidad vendida")

plt.show()
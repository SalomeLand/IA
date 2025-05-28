import numpy as np
from perceptron import Perceptron

# Datos para la función lógica AND
X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

y = np.array([0, 0, 0, 1])  # Salida AND

# Crear el perceptrón, entrenar y predecir
p = Perceptron(learning_rate=0.1, n_iters=10)
p.fit(X, y)

predicciones = p.predict(X)
print("Predicciones:", predicciones)

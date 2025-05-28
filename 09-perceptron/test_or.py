import numpy as np
from perceptron import Perceptron

X = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

y = np.array([0, 1, 1, 1])  # Salida OR

p = Perceptron(learning_rate=0.1, n_iters=10)
p.fit(X, y)

predicciones = p.predict(X)
print("Predicciones:", predicciones)

import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
from sklearn.metrics import confusion_matrix
import seaborn as sns

# Cargar y normalizar datos
(datos_entrenamiento, etiquetas_entrenamiento), (datos_prueba, etiquetas_prueba) = tf.keras.datasets.mnist.load_data()
datos_entrenamiento, datos_prueba = datos_entrenamiento / 255.0, datos_prueba / 255.0

# Definir modelo
clasificador = models.Sequential([
    layers.Flatten(input_shape=(28, 28)),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])
clasificador.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
clasificador.fit(datos_entrenamiento, etiquetas_entrenamiento, epochs=5, validation_split=0.1)

# Evaluación
perdida, precision = clasificador.evaluate(datos_prueba, etiquetas_prueba)
print(f"Precisión del modelo: {precision * 100:.2f}%")

# Predicciones
resultados = clasificador.predict(datos_prueba)
etiquetas_predichas = np.argmax(resultados, axis=1)

# Función para mostrar matriz de confusión
def mostrar_matriz_confusion():
    matriz_conf = confusion_matrix(etiquetas_prueba, etiquetas_predichas)
    plt.figure(figsize=(10, 8))
    sns.heatmap(matriz_conf, annot=True, fmt="d", cmap="YlGnBu", cbar=False,
                xticklabels=range(10), yticklabels=range(10))
    plt.title("Matriz de Confusión - MNIST")
    plt.xlabel("Etiqueta Predicha")
    plt.ylabel("Etiqueta Verdadera")
    plt.show()

# Función para mostrar tabla de conteo
def ver_distribucion_etiquetas():
    conteos = [np.sum(etiquetas_prueba == digito) for digito in range(10)]
    tabla = pd.DataFrame({
        'Dígito': list(range(10)),
        'Total de Imágenes': conteos
    })

    ventana_tabla = tk.Toplevel()
    ventana_tabla.title("Distribución de Imágenes por Dígito")
    tabla_vista = ttk.Treeview(ventana_tabla, columns=("Dígito", "Total"), show='headings')
    tabla_vista.heading("Dígito", text="Dígito")
    tabla_vista.heading("Total", text="Total de Imágenes")
    for digito in range(10):
        tabla_vista.insert("", "end", values=(digito, conteos[digito]))
    tabla_vista.pack(expand=True, fill='both')

# Interfaz gráfica
app = tk.Tk()
app.title("Visualización de MNIST")
app.geometry("400x200")

boton_matriz = tk.Button(app, text="Ver Matriz de Confusión", command=mostrar_matriz_confusion, height=2)
boton_matriz.pack(pady=10)

boton_tabla = tk.Button(app, text="Ver Conteo por Dígito", command=ver_distribucion_etiquetas, height=2)
boton_tabla.pack(pady=10)

app.mainloop()

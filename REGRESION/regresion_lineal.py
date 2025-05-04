import requests
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

# Función para obtener información de la API
def obtener_informacion():
    url = "https://dummyjson.com/users?limit=100"
    respuesta = requests.get(url)
    datos = respuesta.json()
    
    edades = []
    ingresos = []
    nombres_completos = []
    ocupaciones = []
    paises_residencia = []
    
    for usuario in datos['users']:
        edad = usuario['age']
        nombre_completo = f"{usuario['firstName']} {usuario['lastName']}"
        ocupacion = usuario['company']['title']
        pais_residencia = usuario['address']['country']
        
        # Ingreso simulado
        ingreso = edad * 1000 + np.random.randint(-5000, 5000)
        
        edades.append(edad)
        ingresos.append(ingreso)
        nombres_completos.append(nombre_completo)
        ocupaciones.append(ocupacion)
        paises_residencia.append(pais_residencia)
    
    return np.array(edades), np.array(ingresos), nombres_completos, ocupaciones, paises_residencia

# Clase de Perceptrón Lineal
class PerceptronLineal:
    def __init__(self, tasa_aprendizaje=0.000001, iteraciones=1000):
        self.tasa_aprendizaje = tasa_aprendizaje
        self.iteraciones = iteraciones

    def entrenar(self, X, y):
        self.pesos = np.zeros(X.shape[1] + 1)  # +1 por el bias
        for _ in range(self.iteraciones):
            for xi, objetivo in zip(X, y):
                salida = self.predecir(xi)
                error = objetivo - salida
                self.pesos[1:] += self.tasa_aprendizaje * error * xi
                self.pesos[0] += self.tasa_aprendizaje * error  # Bias
    
    def entrada_neta(self, X):
        return np.dot(X, self.pesos[1:]) + self.pesos[0]
    
    def predecir(self, X):
        return self.entrada_neta(X)

# Obtener la información
edades, ingresos, nombres_completos, ocupaciones, paises_residencia = obtener_informacion()
edades = edades.reshape(-1, 1)  # Solo una característica: edad

# Crear el modelo y entrenarlo
modelo_perceptron = PerceptronLineal(tasa_aprendizaje=0.000001, iteraciones=50)
modelo_perceptron.entrenar(edades, ingresos)

# Función para mostrar la gráfica
def mostrar_grafico():
    ingresos_pred = modelo_perceptron.predecir(edades)
    
    plt.scatter(edades, ingresos, color='blue', label='Datos reales')
    plt.plot(edades, ingresos_pred, color='red', label='Línea del perceptrón lineal')
    plt.xlabel('Edad')
    plt.ylabel('Ingreso (USD)')
    plt.title('Perceptrón Lineal - Edad vs Ingreso')
    plt.legend()
    plt.grid(True)
    
    # Mostrar ecuación
    pendiente = modelo_perceptron.pesos[1]
    interseccion = modelo_perceptron.pesos[0]
    plt.text(min(edades), max(ingresos), f"y = {pendiente:.2f}x + {interseccion:.2f}", fontsize=10, color='green')
    
    plt.show()

# Función para mostrar el listado
def mostrar_lista():
    ventana_lista = tk.Toplevel(ventana_principal)
    ventana_lista.title("Listado de Información")
    ventana_lista.geometry("800x500")
    
    tree = ttk.Treeview(ventana_lista, columns=("Nombre Completo", "Edad", "Ingreso", "Ocupación", "País de Residencia"), show="headings")
    
    tree.heading("Nombre Completo", text="Nombre Completo")
    tree.heading("Edad", text="Edad")
    tree.heading("Ingreso", text="Ingreso (USD)")
    tree.heading("Ocupación", text="Ocupación")
    tree.heading("País de Residencia", text="País de Residencia")
    
    for edad, ingreso, nombre_completo, ocupacion, pais_residencia in zip(edades.flatten(), ingresos, nombres_completos, ocupaciones, paises_residencia):
        tree.insert("", tk.END, values=(nombre_completo, edad, f"${ingreso:,.2f}", ocupacion, pais_residencia))
    
    tree.pack(expand=True, fill='both')

# Crear ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Perceptrón Lineal con Datos Reales")
ventana_principal.geometry("320x220")

label_info = tk.Label(ventana_principal, text="Edad vs Ingreso\n(datos de dummyjson)")
label_info.pack(pady=10)

btn_grafico = tk.Button(ventana_principal, text="Mostrar gráfico", command=mostrar_grafico)
btn_grafico.pack(pady=5)

btn_lista = tk.Button(ventana_principal, text="Mostrar listado de información", command=mostrar_lista)
btn_lista.pack(pady=5)

ventana_principal.mainloop()

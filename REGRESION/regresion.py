import requests
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
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

# Obtener la información
edades, ingresos, nombres_completos, ocupaciones, paises_residencia = obtener_informacion()
edades = edades.reshape(-1, 1)

# Crear el modelo y entrenarlo
modelo_regresion = LinearRegression()
modelo_regresion.fit(edades, ingresos)

# Función para mostrar la gráfica
def mostrar_grafico():
    ingresos_pred = modelo_regresion.predict(edades)
    
    plt.scatter(edades, ingresos, color='blue', label='Datos reales')
    plt.plot(edades, ingresos_pred, color='red', label='Línea de regresión')
    plt.xlabel('Edad')
    plt.ylabel('Ingreso (USD)')
    plt.title('Regresión Lineal - Edad vs Ingreso')
    plt.legend()
    plt.grid(True)
    
    pendiente = modelo_regresion.coef_[0]
    interseccion = modelo_regresion.intercept_
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
    
    # Insertar la información
    for edad, ingreso, nombre_completo, ocupacion, pais_residencia in zip(edades.flatten(), ingresos, nombres_completos, ocupaciones, paises_residencia):
        tree.insert("", tk.END, values=(nombre_completo, edad, f"${ingreso:,.2f}", ocupacion, pais_residencia))
    
    tree.pack(expand=True, fill='both')

# Crear ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Regresión Lineal con Datos Reales")
ventana_principal.geometry("320x220")

label_info = tk.Label(ventana_principal, text="Edad vs Ingreso\n(datos de dummyjson)")
label_info.pack(pady=10)

btn_grafico = tk.Button(ventana_principal, text="Mostrar gráfico", command=mostrar_grafico)
btn_grafico.pack(pady=5)

btn_lista = tk.Button(ventana_principal, text="Mostrar listado de información", command=mostrar_lista)
btn_lista.pack(pady=5)

ventana_principal.mainloop()

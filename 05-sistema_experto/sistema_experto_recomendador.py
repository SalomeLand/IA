import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import random

# Definimos las entradas y salidas del sistema difuso
genero = ctrl.Antecedent(np.arange(0, 11, 1), 'genero')
plataforma = ctrl.Antecedent(np.arange(0, 11, 1), 'plataforma')
tipo_juego = ctrl.Antecedent(np.arange(0, 11, 1), 'tipo_juego')
recomendacion = ctrl.Consequent(np.arange(0, 11, 1), 'recomendacion')

# Le damos forma a los valores posibles de cada variable
genero['accion'] = fuzz.trapmf(genero.universe, [0, 0, 2, 5])
genero['aventura'] = fuzz.trapmf(genero.universe, [2, 4, 6, 8])
genero['estrategia'] = fuzz.trapmf(genero.universe, [5, 8, 10, 10])

plataforma['pc'] = fuzz.trapmf(plataforma.universe, [0, 0, 2, 5])
plataforma['playstation'] = fuzz.trapmf(plataforma.universe, [2, 4, 6, 8])
plataforma['xbox'] = fuzz.trapmf(plataforma.universe, [5, 7, 9, 10])
plataforma['switch'] = fuzz.trapmf(plataforma.universe, [3, 5, 7, 9])

tipo_juego['multijugador'] = fuzz.trapmf(tipo_juego.universe, [0, 0, 2, 5])
tipo_juego['solo'] = fuzz.trapmf(tipo_juego.universe, [5, 7, 10, 10])

# Creamos una escala para ver que tan buena es la recomendacion
recomendacion['muy_baja'] = fuzz.trimf(recomendacion.universe, [0, 0, 2])
recomendacion['baja'] = fuzz.trimf(recomendacion.universe, [1, 3, 5])
recomendacion['media'] = fuzz.trimf(recomendacion.universe, [4, 5.5, 7])
recomendacion['alta'] = fuzz.trimf(recomendacion.universe, [6, 7.5, 9])
recomendacion['muy_alta'] = fuzz.trimf(recomendacion.universe, [8, 10, 10])

# Estas reglas dicen que tan recomendable es un juego segun lo que te gusta
rules = [
    ctrl.Rule(genero['accion'] & plataforma['pc'] & tipo_juego['multijugador'], recomendacion['muy_alta']),
    ctrl.Rule(genero['aventura'] & plataforma['playstation'] & tipo_juego['solo'], recomendacion['alta']),
    ctrl.Rule(genero['estrategia'] & plataforma['pc'], recomendacion['muy_alta']),
    ctrl.Rule(genero['accion'] & plataforma['switch'], recomendacion['media']),
    ctrl.Rule(genero['estrategia'] & plataforma['xbox'], recomendacion['media']),
    ctrl.Rule(genero['aventura'] & tipo_juego['multijugador'], recomendacion['media']),
    ctrl.Rule(genero['accion'] & plataforma['xbox'], recomendacion['alta']),
    ctrl.Rule(plataforma['switch'] & tipo_juego['solo'], recomendacion['media']),
    ctrl.Rule(genero['estrategia'] & tipo_juego['solo'], recomendacion['alta']),
    ctrl.Rule(tipo_juego['multijugador'], recomendacion['baja']),
    ctrl.Rule(tipo_juego['solo'], recomendacion['media']),
]

# Armamos el sistema que va a tomar decisiones
recomendador_ctrl = ctrl.ControlSystem(rules)

# Lista de juegos segun el nivel de recomendacion
juegos_por_rango = {
    "muy_baja": ["Candy Crush", "Flappy Bird", "Subway Surfers"],
    "baja": ["Angry Birds", "Clash of Clans", "Plants vs Zombies"],
    "media": ["Minecraft", "Rocket League", "Fall Guys", "Overcooked"],
    "alta": ["Elden Ring", "The Witcher 3", "Horizon Zero Dawn"],
    "muy_alta": ["Red Dead Redemption 2", "God of War", "Zelda: Breath of the Wild"]
}

# Esta funcion recibe el puntaje y devuelve un juego al azar del grupo correspondiente
def obtener_juego(puntaje):
    if puntaje <= 2.0:
        return random.choice(juegos_por_rango["muy_baja"])
    elif puntaje <= 4.0:
        return random.choice(juegos_por_rango["baja"])
    elif puntaje <= 6.0:
        return random.choice(juegos_por_rango["media"])
    elif puntaje <= 8.0:
        return random.choice(juegos_por_rango["alta"])
    else:
        return random.choice(juegos_por_rango["muy_alta"])

# Esta es la funcion principal que hace todo el trabajo de recomendacion
def obtener_recomendacion(genero_val, plataforma_val, tipo_juego_val):
    recomendador_sim = ctrl.ControlSystemSimulation(recomendador_ctrl)
    recomendador_sim.input['genero'] = genero_val
    recomendador_sim.input['plataforma'] = plataforma_val
    recomendador_sim.input['tipo_juego'] = tipo_juego_val

    try:
        recomendador_sim.compute()
        puntuacion = recomendador_sim.output['recomendacion']
        return obtener_juego(puntuacion)
    except Exception as e:
        print("Hubo un problema al calcular la recomendacion:", e)
        return None

# Inicio del programa, donde se piden los gustos del usuario
print("Sistema Experto: Recomendador de Videojuegos")
try:
    genero_val = float(input("Que genero prefieres? (accion: 0-5, aventura: 0-10, estrategia: 5-10): "))
    plataforma_val = float(input("Que plataforma usas? (PC: 0-5, PlayStation: 0-10, Xbox: 5-10, Switch: 0-10): "))
    tipo_juego_val = float(input("Prefieres juegos multijugador o para un solo jugador? (multijugador: 0-5, solo: 5-10): "))

    juego = obtener_recomendacion(genero_val, plataforma_val, tipo_juego_val)

    if juego:
        print(f"\nJuego recomendado: {juego}")
    else:
        print("\nNo se pudo generar una recomendacion con los valores que ingresaste.")
except ValueError:
    print("Entrada no valida. Asegurate de escribir solo numeros.")

import numpy as np
from queue import PriorityQueue
from itertools import count
import random

class Nodo:
    def __init__(self, matriz, x, y, newX, newY, nivel, padre, movimiento=None):
        self.padre = padre
        self.matriz = [row[:] for row in matriz]
        self.matriz[x][y], self.matriz[newX][newY] = self.matriz[newX][newY], self.matriz[x][y]
        self.nivel = nivel
        self.x = newX
        self.y = newY
        self.movimiento = movimiento  

class Puzzle:
    def __init__(self):
        self.dimension = 3
    
        self.fila = [1, 0, -1, 0]
        self.columna = [0, -1, 0, 1]
        self.direcciones = ["abajo", "izquierda", "arriba", "derecha"]

    def generarTableroAleatorio(self):
        while True:
            numeros = random.sample(range(9), 9)
            if self.es_resoluble(numeros):
                tablero = [numeros[i:i+3] for i in range(0, 9, 3)]
                return tablero

    def es_resoluble(self, numeros):
        inversions = 0
        for i in range(len(numeros)):
            for j in range(i + 1, len(numeros)):
                if numeros[i] != 0 and numeros[j] != 0 and numeros[i] > numeros[j]:
                    inversions += 1
        return inversions % 2 == 0

    def encontrarPosicionCero(self, tablero):
        for i in range(self.dimension):
            for j in range(self.dimension):
                if tablero[i][j] == 0:
                    return i, j
        return -1, -1

    def resolverAEstrella(self, inicial, objetivo, x, y):
        pq = PriorityQueue()
        visitados = set()
        contador = count()
        raiz = Nodo(inicial, x, y, x, y, 0, None, None)
        heuristica = self.heuristica_manhattan(raiz.matriz, objetivo)
        pq.put((heuristica, next(contador), raiz))
        visitados.add(str(np.array(inicial)))

        while not pq.empty():
            _, _, nodo = pq.get()
            if self.esObjetivo(nodo.matriz, objetivo):
                self.imprimirCamino(nodo)
                print(f"\n Solución encontrada en {nodo.nivel} movimientos.")
                return
            for i in range(4):
                nuevoX = nodo.x + self.fila[i]
                nuevoY = nodo.y + self.columna[i]
                if self.esValido(nuevoX, nuevoY):
                    movimiento = f"Mover 0 {self.direcciones[i]}"
                    hijo = Nodo(nodo.matriz, nodo.x, nodo.y, nuevoX, nuevoY, nodo.nivel + 1, nodo, movimiento)
                    estado = str(np.array(hijo.matriz))
                    if estado not in visitados:
                        heuristica = self.heuristica_manhattan(hijo.matriz, objetivo)
                        f = heuristica + hijo.nivel
                        pq.put((f, next(contador), hijo))
                        visitados.add(estado)
        print(" No se encontró una solución.")

    def esValido(self, x, y):
        return 0 <= x < self.dimension and 0 <= y < self.dimension

    def esObjetivo(self, estado, objetivo):
        return estado == objetivo

    def heuristica_manhattan(self, estado, objetivo):
        distancia = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                if estado[i][j] != 0:
                    valor = estado[i][j]
                    for x in range(self.dimension):
                        for y in range(self.dimension):
                            if objetivo[x][y] == valor:
                                distancia += abs(i - x) + abs(j - y)
                                break
        return distancia

    def imprimirCamino(self, nodo):
        camino = []
        while nodo:
            camino.append(nodo)
            nodo = nodo.padre
        camino.reverse()

        for paso in camino:
            if paso.movimiento:
                print(paso.movimiento)
            self.imprimirMatriz(paso.matriz)
            print()

    def imprimirMatriz(self, matriz):
        for fila in matriz:
            print(" ".join(map(str, fila)))

if __name__ == "__main__":
    puzzle = Puzzle()

    inicial = puzzle.generarTableroAleatorio()
    objetivo = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    x, y = puzzle.encontrarPosicionCero(inicial)

    print(" Tablero inicial aleatorio:")
    puzzle.imprimirMatriz(inicial)
    print("\n Resolviendo :")
    puzzle.resolverAEstrella(inicial, objetivo, x, y)

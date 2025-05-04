import numpy as np
from queue import PriorityQueue, Queue

class Nodo:
    def __init__(self, matrix, x, y, newX, newY, nivel, padre):
        self.padre = padre
        self.matriz = [row[:] for row in matrix]
        
        # Intercambiar valores
        self.matriz[x][y], self.matriz[newX][newY] = self.matriz[newX][newY], self.matriz[x][y]
        
        self.costo = float('inf')
        self.nivel = nivel
        self.x = newX
        self.y = newY

class Puzzle:
    def __init__(self):
        self.dimension = 3
        # Movimientos posibles: Abajo, Izquierda, Arriba, Derecha
        self.fila = [1, 0, -1, 0]
        self.columna = [0, -1, 0, 1]

    def depthFirstSearch(self, inicial, objetivo, x, y):
        stack = []
        visitados = set()
        raiz = Nodo(inicial, x, y, x, y, 0, None)
        stack.append(raiz)
        visitados.add(str(np.array(inicial)))

        while stack:
            nodo = stack.pop()
            if self.calcularCosto(nodo.matriz, objetivo) == 0:
                self.imprimirCamino(nodo)
                print(f"Solución encontrada en {nodo.nivel} movimientos!")
                return
            for i in range(4):
                nuevoX = nodo.x + self.fila[i]
                nuevoY = nodo.y + self.columna[i]
                if self.esSeguro(nuevoX, nuevoY):
                    hijo = Nodo(nodo.matriz, nodo.x, nodo.y, nuevoX, nuevoY, nodo.nivel + 1, nodo)
                    estado = str(np.array(hijo.matriz))
                    if estado not in visitados:
                        stack.append(hijo)
                        visitados.add(estado)
        print("No se encontró una solución.")

    def breadthFirstSearch(self, inicial, objetivo, x, y):
        queue = Queue()
        visitados = set()
        raiz = Nodo(inicial, x, y, x, y, 0, None)
        queue.put(raiz)
        visitados.add(str(np.array(inicial)))

        while not queue.empty():
            nodo = queue.get()
            if self.calcularCosto(nodo.matriz, objetivo) == 0:
                self.imprimirCamino(nodo)
                print(f"Solución encontrada en {nodo.nivel} movimientos!")
                return
            for i in range(4):
                nuevoX = nodo.x + self.fila[i]
                nuevoY = nodo.y + self.columna[i]
                if self.esSeguro(nuevoX, nuevoY):
                    hijo = Nodo(nodo.matriz, nodo.x, nodo.y, nuevoX, nuevoY, nodo.nivel + 1, nodo)
                    estado = str(np.array(hijo.matriz))
                    if estado not in visitados:
                        queue.put(hijo)
                        visitados.add(estado)
        print("No se encontró una solución.")

    def uniformCostSearch(self, inicial, objetivo, x, y):
        pq = PriorityQueue()
        visitados = set()
        raiz = Nodo(inicial, x, y, x, y, 0, None)
        pq.put((raiz.nivel, raiz))
        visitados.add(str(np.array(inicial)))

        while not pq.empty():
            _, nodo = pq.get()
            if self.calcularCosto(nodo.matriz, objetivo) == 0:
                self.imprimirCamino(nodo)
                print(f"Solución encontrada en {nodo.nivel} movimientos!")
                return
            for i in range(4):
                nuevoX = nodo.x + self.fila[i]
                nuevoY = nodo.y + self.columna[i]
                if self.esSeguro(nuevoX, nuevoY):
                    hijo = Nodo(nodo.matriz, nodo.x, nodo.y, nuevoX, nuevoY, nodo.nivel + 1, nodo)
                    estado = str(np.array(hijo.matriz))
                    if estado not in visitados:
                        pq.put((hijo.nivel, hijo))
                        visitados.add(estado)
        print("No se encontró una solución.")

    def esSeguro(self, x, y):
        return 0 <= x < self.dimension and 0 <= y < self.dimension

    def calcularCosto(self, inicial, objetivo):
        contador = 0
        for i in range(len(inicial)):
            for j in range(len(inicial)):
                if inicial[i][j] != 0 and inicial[i][j] != objetivo[i][j]:
                    contador += 1
        return contador

    def imprimirCamino(self, raiz):
        if raiz is None:
            return
        self.imprimirCamino(raiz.padre)
        self.imprimirMatriz(raiz.matriz)
        print()

    def imprimirMatriz(self, matriz):
        for fila in matriz:
            print(" ".join(map(str, fila)))

if __name__ == "__main__":
    inicial = [
        [1, 8, 2],
        [0, 4, 3],
        [7, 6, 5]
    ]
    objetivo = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    x, y = 1, 0
    
    puzzle = Puzzle()
    opcion = int(input("Seleccione el algoritmo de búsqueda:\n1. DFS\n2. BFS\n3. Costo Uniforme\nOpción: "))
    
    if opcion == 1:
        puzzle.depthFirstSearch(inicial, objetivo, x, y)
    elif opcion == 2:
        puzzle.breadthFirstSearch(inicial, objetivo, x, y)
    elif opcion == 3:
        puzzle.uniformCostSearch(inicial, objetivo, x, y)
    else:
        print("Opción no válida")

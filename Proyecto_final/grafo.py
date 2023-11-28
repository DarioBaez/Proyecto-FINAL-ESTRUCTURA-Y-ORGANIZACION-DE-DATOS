import sqlite3
class Arista():
    def __init__(self, Nodo1, Nodo2, Peso):
        self.Nodo1 = Nodo1
        self.Nodo2 = Nodo2
        self.Peso = Peso

class Grafo():
    def __init__(self):
        self.nodos = set()
        self.aristas = []

    def AgregarArista(self, Arista):
        self.aristas.append(Arista)
        self.nodos.add(Arista.Nodo1)
        self.nodos.add(Arista.Nodo2)













import os
import random
import time
import threading

inicioPuente = 10
largoPuente = 20

cantVacas = 5

class Vaca(threading.Thread):
    def __init__(self, sem):
        super().__init__()
        self.posicion = 0
        self.velocidad = random.uniform(0.1, 0.9)
        self.semaforo = sem

    def avanzar(self):
        if inicioPuente <= self.posicion <= (inicioPuente+largoPuente):
            self.semaforo.acquire()
            try:
                time.sleep(1-self.velocidad)
                self.posicion += 1
            finally:
                self.semaforo.release()
        else:
            time.sleep(1-self.velocidad)
            self.posicion += 1
    
            
    def dibujar(self):
        print(' ' * self.posicion + '🐮') # si no funciona, cambiá por 'V'

    def run(self):
        while(True):
            self.avanzar()

vacas = []
sem = threading.Semaphore(1)
for i in range(cantVacas):
    v = Vaca(sem)
    vacas.append(v)
    v.start() # si la clase hereda de Thread, el .start() siempre corre run() de la clase.

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def dibujarPuente():
    print(' ' * inicioPuente + '=' * largoPuente)

while(True):
    cls()
    print('Apretá Ctrl + C varias veces para salir...')
    print()
    dibujarPuente()
    for v in vacas:
        v.dibujar()
    dibujarPuente()
    time.sleep(0.2)
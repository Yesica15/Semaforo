import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class Cocinero(threading.Thread):
    def __init__(self, numero, cocineroSem, comensalSem):
        super().__init__()
        self.name = f'Cocinero {numero}'
        self.cocineroBlock = cocineroSem
        self.comensalBlock = comensalSem

    def run(self):
        global platosDisponibles
        while (True):
            self.cocineroBlock.acquire()
            try:
                logging.info('Reponiendo los platos...')
                platosDisponibles = 3
            finally:
                self.comensalBlock.release()

class Comensal(threading.Thread):
    def __init__(self, numero, cocineroSem, comensalSem):
        super().__init__()
        self.name = f'Comensal {numero}'
        self.cocineroBlock = cocineroSem
        self.comensalBlock = comensalSem

    def run(self):
        global platosDisponibles
        
        self.comensalBlock.acquire()
        try: 
            while platosDisponibles==0:
                self.cocineroBlock.release()
                self.comensalBlock.acquire()
            platosDisponibles -= 1
            logging.info(f'¡Qué rico! Quedan {platosDisponibles} platos')
        finally:
            self.comensalBlock.release()

platosDisponibles = 3

cocineroSem = threading.Semaphore(0)
comensalSem = threading.Semaphore(1)

for i in range(5):
    Cocinero(i, cocineroSem,comensalSem).start()

for i in range(30):
    Comensal(i, cocineroSem, comensalSem).start()



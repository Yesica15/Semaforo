import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

lock = threading.Lock()
llamado = True

class Cocinero(threading.Thread):
    def __init__(self, cocineroSem, comensalSem):
        super().__init__()
        self.name = 'Cocinero'
        self.cocineroBlock = cocineroSem
        self.comensalBlock1 = comensalSem

    def run(self):
        global platosDisponibles
        global llamado
        while (True):
            self.cocineroBlock.acquire()
            try:
                logging.info('Reponiendo los platos...')
                platosDisponibles = 4
                llamado = True
            finally:
                self.comensalBlock1.release()

class Comensal(threading.Thread):
    def __init__(self, numero, cocineroSem, comensalSem):
        super().__init__()
        self.name = f'Comensal {numero}'
        self.cocineroBlock = cocineroSem
        self.comensalBlock1 = comensalSem

    def run(self):
        global platosDisponibles
        global llamado
        global lock
        self.comensalBlock1.acquire()
        try: 
            while platosDisponibles==0:
                if llamado==True and platosDisponibles==0:
                    lock.acquire()
                    try:
                        llamado = False
                        self.cocineroBlock.release()
                        self.comensalBlock1.acquire() 
                    finally:
                        lock.release()  
            platosDisponibles -= 1
            logging.info(f'¡Qué rico! Quedan {platosDisponibles} platos')
        finally:
            self.comensalBlock1.release()
        
platosDisponibles = 4

cocineroSem = threading.Semaphore(0)
comensalSem1 = threading.Semaphore(2)

Cocinero(cocineroSem,comensalSem1).start()

for i in range(40):
    Comensal(i, cocineroSem, comensalSem1).start()


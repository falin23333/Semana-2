import threading
import time


def proceso1():
    print("Iniciando proceso 1...")
    time.sleep(3)
    print("Proceso 1 finalizado")


def proceso2():
    print("Iniciando proceso 2...")
    time.sleep(2)
    print("Proceso 2 finalizado")


def proceso3():
    print("Iniciando proceso 3...")
    time.sleep(3)
    print("Proceso 3 finalizado")

inicio = time.perf_counter()

for proceso in [proceso1,proceso2,proceso3]:
    process = threading.Thread(target=proceso,args=())
    process.start()  # inicia el proceso
    
for proceso in [proceso1,proceso2,proceso3]:
    proceso.join()    
process.join()   # hasta que no termine el proceso no continua ejecutando

print(threading.active_count()) # numero hilos concurrentes
print(threading.enumerate())  

fin = time.perf_counter()

print(fin-inicio)
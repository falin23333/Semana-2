

# Enunciado actividad

# A11 A12
# A21 A22

# B11 B12
# B21 B22

# C11=(A11*B11 + A12*B21)    C12=(A11*B12 + A12*B22)
# C21=(A21*B11 + A22*B21)    C22=(A21*B12 + A22*B22)

import time
import threading
import numpy as np
from numpy.random import seed
from numpy.random import rand
def intro():
    print("""
┏┓      ┓  ┓•             ┏┓•            ┳┓•    •┓   • ┓   
┃┃┏┓┏┓┏┓┃┏┓┃┓┏┏┳┓┏┓┏  ┓┏  ┗┓┓┏╋┏┓┏┳┓┏┓┏  ┃┃┓┏╋┏┓┓┣┓┓┏┓┏┫┏┓┏
┣┛┗┻┛ ┗┻┗┗ ┗┗┛┛┗┗┗┛┛  ┗┫  ┗┛┗┛┗┗ ┛┗┗┗┻┛  ┻┛┗┛┗┛ ┗┗┛┗┻┗┗┻┗┛┛
                       ┛                                   

          Actividad 2 Francisco Javier Duque García , Rafael Cañada Abolafia y Pablo Sánchez Arias\n\n\n
          
    1º Modificar el programa de multiplicación de matrices para que todas las funciones paralelas sean ejecutadas en un thread\n
    Implementar una versión donde se hagan todas las multiplicaciones primero y luego se
    realicen las sumas de los diferentes bloques en funciones diferentes.
          
    
          """)
def Crea_bloque(N,M):
        N = N # Numero de bloques
        M = M # Tamaño de los bloques

        seed(10)

        A_bloques = []
        B_bloques = []

        for i in range(N):
            fila_A = []
            fila_B = []
            for j in range(N):
                fila_A.append(rand(M, M))
                fila_B.append(rand(M, M))
            A_bloques.append(fila_A)
            B_bloques.append(fila_B)

        

        

        A = np.block(A_bloques)
        B = np.block(B_bloques)
        print("Matrices Generadas.\n")
        print(f"A = {A}")
        print("\n")
        print(f"B = {B}\n\n")
        return A,B,A_bloques,B_bloques


def Antes_De_Sumar_Bloques_Verifica_que_TODOS_los_Hilos_Finalizaron(C_hilos):
    n = 0
    for fila_hilos in C_hilos:
            for filaa in fila_hilos:
                filaa.join()
                n+=1
    return n


def suma_bloques(bloques):
    acu = bloques[0][0]                                                     # primera suma de los bloques
    for bloque in bloques[1:][0]:
        acu += bloque                                                       # voy acumulando hasta fin array
    return acu
     

def multiply(A, B,C_sol_fila):
    res = np.zeros((A.shape[0], A.shape[1]))  

    for k in range(A.shape[0]):
        for i in range(B.shape[1]):            
            for j in range(A.shape[1]):
                #print("---")
                #print(f"{A[k][j]} x {B[j][i]} = {A[k][j] * B[j][i]}")
                res[k, i] += A[k][j] * B[j][i]                              # Multiplica filas x columnas entre bloques
                                                                            # Por ejemplo A11 = [[1 2],  *   B12 = [[5 6],   = (1*5) + (2*7)
                                                                            #                    [3,4]]             [7 8]]
    C_sol_fila.append(res)                                                  # Pasamos resultado


def multiply_bloques(A_bl, B_bl):
    C_sol = []
    C_hilos = []
    N = len(A_bl)
    fila_x_columna = []
    n_hilos = 0                                                                             # para contar los hilos totales
    for k in range(N):
                              
        for i in range(N):
            C_sol_fila = []
            hilo_fila = []
            for j in range(N):
                C_sol_fila.append([])                                                       # Pasamos como parámetros los bloques Aij y Bij y los multiplicamos, guardando en C_sol_fila
                hilo_fila.append(
                    threading.Thread(
                        target=multiply,args=(A_bl[k][j], B_bl[j][i],C_sol_fila[-1])        # Por ejemplo multiply(A11,B11) , multiply(A11,B12) ......
                    )
                )    
                hilo_fila[-1].start()
                """print(f"A_bl{k}{j} * B_bl{j}{i}")                    # DISEÑO OUTPUTS
                if j < N-1:                                             # DISEÑO OUTPUTS
                    print("+")                                          # DISEÑO OUTPUTS
            print("\n---")"""  
            C_hilos.append(hilo_fila)                                            # DISEÑO OUTPUTS
            n_hilos += Antes_De_Sumar_Bloques_Verifica_que_TODOS_los_Hilos_Finalizaron(C_hilos)
            fila_x_columna.append(C_sol_fila)
            #aux = suma_bloques(C_sol_fila)
            #fila.append(aux)
            
        C_sol.append(fila_x_columna)            
    print(f"\n\nSe han generado y ejecutado un total de {n_hilos} hilos de multiplicaciones\n\n")
    return fila_x_columna
def suma_filas_generadas(solucion_bloques,N,M):
    Csol = []
    for i in range(0, N * M, M):
        suma_filas = []
        for j in range(len (solucion_bloques[i])):
            print(solucion_bloques[i])
            suma_filas.append(suma_bloques(solucion_bloques[j+i]))  # Suma todos los resultados de las multiplicaciones de las filas y cuando sale de este bloque se pasa a la siguiente fila
        Csol.append(suma_filas)
    return Csol



if __name__ == '__main__':
    intro()                                                     # Presentación Actividad
    
    N = int(input("Introduce nº bloques :"))                                                       # Numero de bloques
    M = int(input("Introduce tamaño de los bloque :"))                                                       # Tamaño de los bloques
                                  
    A,B, A_bloques, B_bloques = Crea_bloque(N,M)                # Inicializacion matrices, bloques
    
    ########################################################
    inicio = time.perf_counter()

    solucion_bloques = multiply_bloques(A_bloques, B_bloques)   # Solución Multiplicación Matrices python puro
    Cij = suma_filas_generadas(solucion_bloques,N,M)              # Suma las multiplicaciones de cada fila y genera Cij FINAL
    
    fin = time.perf_counter()
    ########################################################
    
    print(f"Tiempo de ejecución: {fin-inicio}sg")
    
    print("\nSolucion Multiplicación Matrices python puro\n")
    print(np.block(Cij))
    print("Solucion libreria numpy\n")
    print(np.matmul(A, B))
    

    if np.allclose(np.matmul(A, B), np.block(Cij)) == True:
        print("\n\n\nTest Verificación correcta")
    else:
        print("\n\n\nTest Verificación incorrecta")

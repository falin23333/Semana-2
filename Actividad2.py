

# Enunciado actividad

# A11 A12
# A21 A22

# B11 B12
# B21 B22

# C11=(A11*B11 + A12*B21)    C12=(A11*B12 + A12*B22)
# C21=(A21*B11 + A22*B21)    C22=(A21*B12 + A22*B22)
# 27:43, no mejora el algotimo etc etc

import threading
import time
import numpy as np
from numpy.random import seed
from numpy.random import rand
def intro():
    print("""
┏┓      ┓  ┓•             ┏┓•            ┳┓•    •┓   • ┓   
┃┃┏┓┏┓┏┓┃┏┓┃┓┏┏┳┓┏┓┏  ┓┏  ┗┓┓┏╋┏┓┏┳┓┏┓┏  ┃┃┓┏╋┏┓┓┣┓┓┏┓┏┫┏┓┏
┣┛┗┻┛ ┗┻┗┗ ┗┗┛┛┗┗┗┛┛  ┗┫  ┗┛┗┛┗┗ ┛┗┗┗┻┛  ┻┛┗┛┗┛ ┗┗┛┗┻┗┗┻┗┛┛
                       ┛                                   

          Actividad 1 Francisco Javier Duque García y Rafael Cañada Abolafia\n\n\n
          
    1º Programar un algoritmo de multiplicación de matrices cuadradas de igual tamaño\n
    2º Realizar una versión por bloques del anterior algoritmo\n
    3º Realizar un test para verificar que los resultados de los algoritmos 1 y 2 son iguales
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
    for fila_hilos in C_hilos:
                for filaa in fila_hilos:
                    filaa.join()


def suma_bloques(bloques):
    
    acu = bloques[0]                      # primera suma de los bloques
    for bloque in bloques[1:]:
        acu += bloque                       # voy acumulando hasta fin array
    return acu 

def multiply(A, B,lista_resultado):
    T = len(A)
    resultado = np.zeros((T, T))
    for i in range(T):
        for j in range(T):
            valor_actual = 0
            # Inicializar un bloque zeros((M, M))
            for k in range(T):
                
                valor_actual += A[i][k] * B[k][j]
                
            resultado[i][j] = valor_actual
    
    lista_resultado.append(resultado)
    

                                                                  # Pasamos resultado
def Lanza_Multiplicaciones_Matrices_Threading(A_bl,B_bl):
    C_sol = []
    C_hilos = []
    N = len(A_bl)

    for k in range(N):
                              
        for i in range(N):
            fila = []
            C_sol_fila = []
            threading_fila = []
            for j in range(N):
                C_sol_fila.append([])
                threading_fila.append(
                    threading.Thread(
                        target=multiply,
                        args=(A_bl[k][j], B_bl[j][i],C_sol_fila[-1])
                        )                                             # Pasamos como parámetros los bloques Aij y Bij y los multiplicamos, guardando en C_sol_fila,# Por ejemplo multiply(A11,B11) , multiply(A11,B12) ......
                )
                
                threading_fila[-1].start()                            # no sabemos el orden del hilo que se ejecuta, a partir de aqui ya puede ir ejecutando los hilos, no sabemos el orden de los hilos
                """#C_sol_fila.append(multiply(A_bl[k][j], B_bl[j][i]))     
                print(f"A_bl{k}{j} * B_bl{j}{i}")                       # DISEÑO OUTPUTS
                if j < N-1:                                             # DISEÑO OUTPUTS
                    print("+")                                          # DISEÑO OUTPUTS
            print("\n---")"""
            C_hilos.append(threading_fila)
            Antes_De_Sumar_Bloques_Verifica_que_TODOS_los_Hilos_Finalizaron(C_hilos) # Importante, si no ejecutamos esta linea puede dar cualquier cosa, para garantizar le orden de las sumas es necesiario hacer join() , y así garantizar que se multiplicaron los bloques antes de sumar
            C_sol_fila = [x[0] for x in C_sol_fila]
            fila.append(suma_bloques(C_sol_fila))
            C_sol.append(fila) # ahora ya podemos sumar los bloques para calcula el Cij
    
    print(C_sol)
    return C_sol                                           # DISEÑO OUTPUT

def multiply_bloques(A_bl, B_bl):
    Soluciones_Multiplicaciones = Lanza_Multiplicaciones_Matrices_Threading(A_bl,B_bl)
    print(np.block(Soluciones_Multiplicaciones))
    

    
    
    

if __name__ == '__main__':
    intro()                                                     # Presentación Actividad
    
    A,B, A_bloques, B_bloques = Crea_bloque(2,2)                # Inicializacion matrices, bloques
    print(np.matmul(A, B))
    
    solucion_bloques = multiply_bloques(A_bloques, B_bloques)   # Solución Multiplicación Matrices python puro
    C_solucion = np.matmul(A, B)                                # Solución con libreria Numpy
    print(np.block(solucion_bloques))

    
    
    print("Solucion Multiplicación Matrices python puro\n")
    print(np.block(solucion_bloques))
    print("Solucion libreria numpy\n")
    print(C_solucion)
    
    if np.allclose(C_solucion, np.block(solucion_bloques)) == True:
        print("\n\n\nTest Verificación correcta")
    else:
        print("\n\n\nTest Verificación incorrecta")

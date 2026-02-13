

# Enunciado actividad

# A11 A12
# A21 A22

# B11 B12
# B21 B22

# C11=(A11*B11 + A12*B21)    C12=(A11*B12 + A12*B22)
# C21=(A21*B11 + A22*B21)    C22=(A21*B12 + A22*B22)


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
    acu = bloques[0][0]                        # primera suma de los bloques
    for bloque in bloques[1:][0]:
        acu += bloque                       # voy acumulando hasta fin array
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

    C_sol_fila.append(res)                                                              # Pasamos resultado


def multiply_bloques(A_bl, B_bl):
    C_sol = []
    C_hilos = []
    N = len(A_bl)

    for k in range(N):
        fila = []                      
        for i in range(N):
            C_sol_fila = []
            hilo_fila = []
            for j in range(N):
                C_sol_fila.append([])                                                        # Pasamos como parámetros los bloques Aij y Bij y los multiplicamos, guardando en C_sol_fila
                hilo_fila.append(
                    threading.Thread(
                        target=multiply,args=(A_bl[k][j], B_bl[j][i],C_sol_fila[-1])        # Por ejemplo multiply(A11,B11) , multiply(A11,B12) ......
                    )
                )    
                hilo_fila[-1].start()
                """print(f"A_bl{k}{j} * B_bl{j}{i}")                       # DISEÑO OUTPUTS
                if j < N-1:                                             # DISEÑO OUTPUTS
                    print("+")                                          # DISEÑO OUTPUTS
            print("\n---")"""  
            C_hilos.append(hilo_fila)                                            # DISEÑO OUTPUTS
            Antes_De_Sumar_Bloques_Verifica_que_TODOS_los_Hilos_Finalizaron(C_hilos)
            aux = suma_bloques(C_sol_fila)
            fila.append(aux)
            
        C_sol.append(fila)            

    return C_sol

if __name__ == '__main__':
    intro()                                                     # Presentación Actividad
    A,B, A_bloques, B_bloques = Crea_bloque(2,2)                # Inicializacion matrices, bloques
    
    
    solucion_bloques = multiply_bloques(A_bloques, B_bloques)   # Solución Multiplicación Matrices python puro
    C_solucion = np.matmul(A, B)                                # Solución con libreria Numpy
    

    
    
    print("Solucion Multiplicación Matrices python puro\n")
    print(np.block(solucion_bloques))
    print("Solucion libreria numpy\n")
    print(C_solucion)
    
    if np.allclose(C_solucion, np.block(solucion_bloques)) == True:
        print("\n\n\nTest Verificación correcta")
    else:
        print("\n\n\nTest Verificación correcta")

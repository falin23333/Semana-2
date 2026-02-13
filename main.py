# Actividades - np.dot
# Videoconferencias - np.multiply


# (6x6) x (6x6) = (6x6)


# (AxB) x (BxC) = (AxC)
# (7 x 4) x (4 x 6) = (7 x 6)

# Descomposición de matrices

# 1 2 3 4
# 5 6 7 8
# 9 0 1 2
# 3 4 5 6


# 1 2    3 4
# 5 6    7 8

# 9 0    1 2
# 3 4    5 6

#
# A11 A12
# A21 A22
#
# A11 =
# 1 2
# 5 6
#
# A12 =
# 3 4
# 7 8
#
# A21 =
# 9 0
# 3 4
#
# A22 =
# 1 2
# 5 6

# Enunciado actividad

# A11 A12
# A21 A22

# B11 B12
# B21 B22

# C11=(A11*B11 + A12*B21)    C12=(A11*B12 + A12*B22)
# C21=(A21*B11 + A22*B21)    C22=(A21*B12 + A22*B22)

# A11*B11 <- C11
# A12*B21 <- C11
# A11*B12 <- C12
# A12*B22 <- C12
# A21*B11 <- C21
# A22*B21 <- C21
# A21*B12 <- C22
# A22*B22 <- C22

# Enunciado videoconferencias

# C11=(A11*B11)    C12=(A12*B12)
# C21=(A21*B21)    C22=(A22*B22)

import numpy as np
from numpy.random import seed
from numpy.random import rand
import threading

def multiply(A, B, lista_resultado):
    C_num = []
    for i in range(A.shape[0]):
        C_num_fila = []
        for j in range(A.shape[1]):
            C_num_fila.append(A[i][j] * B[i][j])
        C_num.append(C_num_fila)
    lista_resultado.append(np.array(C_num))

def acumular_bloques(lista_de_bloques):
    tamano_del_bloque = lista_de_bloques[0].shape[0]
    resultado_actual = np.zeros((tamano_del_bloque, tamano_del_bloque))
    for bloque in lista_de_bloques:
        resultado_actual += bloque
    lista_de_bloques.clear()
    lista_de_bloques.append(resultado_actual)

def multiply_bloques(A_bl, B_bl):
    C_sol = []
    C_hilos = []
    for i in range(len(A_bl)):
        C_sol_fila = []
        C_hilo_fila = []
        for j in range(len(A_bl[0])):
            C_sol_fila.append([])
            C_hilo_fila.append(
                threading.Thread(
                    target=multiply,
                    args=(A_bl[i][j], B_bl[i][j], C_sol_fila[-1])
                )
            )
            C_hilo_fila[-1].start()
            # A_bl[i][k], B_bl[k][j]
        C_sol.append(C_sol_fila)
        C_hilos.append(C_hilo_fila)

    # Aqui espero
    for fila_hilos in C_hilos:
        for hilo in fila_hilos:
            hilo.join()

    # Todos los hilos han acabado
    for i in range(len(C_sol)):
        for j in range(len(C_sol[0])):
            acumular_bloques(C_sol[i][j])

    # Espero

    for i in range(len(C_sol)):
        for j in range(len(C_sol[0])):
            C_sol[i][j] = C_sol[i][j][0]
    # Esperar a todos los calculos

    return C_sol

if __name__ == '__main__':
    N = 2 # Numero de bloques
    M = 3 # Tamaño de los bloques

    seed(1)

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

    ## Hasta aquí, el código es común con la actividad

    print(A_bloques)
    print(B_bloques)

    A = np.block(A_bloques)
    B = np.block(B_bloques)

    C_solucion = np.multiply(A, B)
    # Actividad -> np.dot

    solucion_bloques = multiply_bloques(A_bloques, B_bloques)

    print(np.allclose(C_solucion, np.block(solucion_bloques)))

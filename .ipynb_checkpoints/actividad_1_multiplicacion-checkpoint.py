import numpy as np
from numpy.random import rand
from numpy.random import seed

seed(23)


def dot_bloque(A, B):
    T = len(A)
    resultado = np.zeros((T, T))
    for i in range(T):
        for j in range(T):
            valor_actual = 0
            # Inicializar un bloque zeros((M, M))
            for k in range(T):
                valor_actual += A[i][k] * B[k][j]
            resultado[i][j] = valor_actual
    return resultado


def dot_bloques(A_bloques, B_bloques):
    T = len(A_bloques)
    M = len(A_bloques[0][0])
    resultado = []
    for i in range(T):
        fila_actual = []
        for j in range(T):
            # Inicializar un bloque zeros((M, M))
            matrices_parciales = []
            for k in range(T):
                matrices_parciales.append(dot_bloque(A_bloques[i][k], B_bloques[k][j]))

            valor_actual = np.zeros((M, M))
            for k in range(len(matrices_parciales)):
                valor_actual += matrices_parciales[k]
            # N^2
            fila_actual.append(valor_actual)
        resultado.append(fila_actual)
    return resultado

if __name__ == '__main__':

    T = 24

    N = 4
    M = 6

    A_bloques = []
    B_bloques = []
    for i in range(N):
        fila_actual_A = []
        fila_actual_B = []
        for j in range(N):
            fila_actual_A.append(rand(M, M))
            fila_actual_B.append(rand(M, M))
        A_bloques.append(fila_actual_A)
        B_bloques.append(fila_actual_B)

    # ACTIVIDAD 1
    A = np.block(A_bloques)
    B = np.block(B_bloques)

    C_practica = np.dot(A, B)
    C_prac_2 = dot_bloque(A, B)
    C_bloques_practica = dot_bloques(A_bloques, B_bloques)
    print("Resultado multiplicacion un bloque: " + str(np.allclose(C_prac_2, C_practica)))
    print("Resultado bloques: " + str(np.allclose(np.block(C_bloques_practica), np.dot(np.block(A_bloques), np.block(B_bloques)))))

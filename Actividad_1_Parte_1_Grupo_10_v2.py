"""
UNIVERSITAT CARLEMANY –  PARALELISMO Y SISTEMAS DISTRIBUIDOS
Profesor: Ramón Amela
GRUPO 10
Rafael Cañada Abolafia
Francisco Javier Duque García
Pablo Sánchez Arias
PARTE 1 - PUNTOS 1, 2 Y 3
"""
"""
Recordatorio para no perderse:
A11 A12
A21 A22

B11 B12
B21 B22

C11=(A11*B11 + A12*B21)    C12=(A11*B12 + A12*B22)
C21=(A21*B11 + A22*B21)    C22=(A21*B12 + A22*B22)
"""
import numpy as np
from numpy.random import seed
from numpy.random import rand


"""
Actividad 1-1
Multiplicación de matrices cuadradas del mismo tamaño usando Python puro.
"""
def mul_puro(A, B):
    n = len(A)  # Sirve tanto para la matriz entera como para un bloque
    C = []      # Matriz resultado que se construye fila a fila

    for i in range(n):              # Recorremos filas de A
        fila = []

        for j in range(n):          # Recorremos columnas de B
            suma = 0.0

            for k in range(n):      # Productos necesarios para C[i][j]
                suma += A[i][k] * B[k][j]

            fila.append(suma)

        C.append(fila)

    return np.array(C)


"""
Actividad 1-2
Multiplicación por bloques.
Cada matriz tiene N x N bloques y cada bloque es de tamaño M x M.
"""
def crear_bloques(N, M):
    A_bloques = []  # Bloques de la matriz A
    B_bloques = []  # Bloques de la matriz B

    for i in range(N):
        fila_A = []
        fila_B = []

        for j in range(N):
            # Cada bloque es una matriz MxM generada aleatoriamente
            fila_A.append(rand(M, M))
            fila_B.append(rand(M, M))

        A_bloques.append(fila_A)
        B_bloques.append(fila_B)

    return A_bloques, B_bloques


def calcular_bloque_Cij(i, j, A_bloques, B_bloques, N, M):
    # Inicializamos el bloque C[i][j] a cero antes de sumar los productos
    C_ij = np.zeros((M, M))

    for k in range(N):
        # Multiplicamos bloques A[i][k] y B[k][j] reutilizando mul_puro
        producto = mul_puro(A_bloques[i][k], B_bloques[k][j])

        # Sumamos el resultado parcial al bloque C[i][j]
        for fi in range(M):
            for fj in range(M):
                C_ij[fi][fj] += producto[fi][fj]

    return C_ij


def mul_por_bloques(A_bloques, B_bloques, N, M):
    C_bloques = []  # Matriz resultado expresada en bloques

    for i in range(N):
        fila = []
        for j in range(N):
            # Cada bloque C[i][j] se calcula de forma independiente
            fila.append(calcular_bloque_Cij(i, j, A_bloques, B_bloques, N, M))
        C_bloques.append(fila)

    return C_bloques


"""
Actividad 1-3
Test para comprobar que ambos métodos dan el mismo resultado.
"""
def test_final(A_bloques, B_bloques, N, M):
    n = N * M  # Tamaño total de la matriz completa

    # Unimos los bloques en matrices completas con numpy.block
    A = np.block(A_bloques)
    B = np.block(B_bloques)

    # Algoritmo 1: multiplicación normal (python puro)
    C1 = mul_puro(A, B)

    # Algoritmo 2: multiplicación por bloques
    C_bloques = mul_por_bloques(A_bloques, B_bloques, N, M)
    C2 = np.block(C_bloques)

    print("Matriz A:")
    print(A)
    print()
    print("Matriz B:")
    print(B)
    print()
    print("Resultado C1 (normal):")
    print(C1)
    print()
    print("Resultado C2 (por bloques):")
    print(C2)
    print()

    # Test: comparar los dos algoritmos entre sí
    if np.allclose(C1, C2):
        print("TEST OK: C1 y C2 coinciden.")
    else:
        print("TEST ERROR: C1 y C2 no coinciden.")

    # Referencia con np.dot (solo en el test, como permite el enunciado)
    C_ref = np.dot(A, B)
    if np.allclose(C1, C_ref):
        print("Referencia OK: C1 coincide con np.dot.")
    else:
        print("Referencia ERROR: C1 no coincide con np.dot.")


if __name__ == "__main__":
    N = 2  # Número de bloques por dimensión
    M = 2  # Tamaño de cada bloque

    seed(1)

    A_bloques, B_bloques = crear_bloques(N, M)
    test_final(A_bloques, B_bloques, N, M)
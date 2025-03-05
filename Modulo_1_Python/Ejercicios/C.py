import numpy as np

A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
B = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])



def producto_matrices(matrizA, matrizB):
    #dimensiones de las matrices
    filasA, columnasA = matrizA.shape
    filasB, columnasB = matrizB.shape

    def mult_fila_columna(A, B, n_fila, n_columna):
        return sum(A[n_fila,:] * B[:,n_columna])

    assert filasA == filasB == columnasA == columnasB

    matrizC = np.zeros((filasA, columnasA))

    for k in range(0, filasA):
        for i in range(0, columnasA):
            #matrizC[k][i] = mult_fila_columna(matrizA, matrizB, k, i)
            # Producto escalar
            matrizC[k][i] = np.inner((matrizA[k,:]),(matrizB[:,i]))
    
    return matrizC

# print(producto_matrices(A, B))

# histograma de la matriz resultante
import matplotlib.pyplot as plt
# plt.hist(producto_matrices(A, B).flatten(), bins=9)
# plt.show()

# Determinante de la matriz regla del corazon
def determinante_corazon(matriz):
    # print(matriz)

    # Quitar la primera fila y ultima fila y primera y ultima columna
    corazon = np.linalg.det(matriz[1:-1, 1:-1])
    # Comprobar que corazon es distinto de 0 devolver true o false
    if corazon != 0:
        esq_sup_izq = matriz[0:-1, 0:-1]
        esq_sup_derecha = matriz[0:-1, 1:]
        esq_inf_izq = matriz[1:, 0:-1]
        esq_inf_derecha = matriz[1:, 1:]

        #inversa corazon
        inversa_corazon = 1/(corazon)

        print("Det: ", matriz, "= (1 / ", corazon, ") * (", esq_sup_izq, " * ", esq_inf_derecha, " - ", esq_inf_izq, " * ", esq_sup_derecha, ")")
        return inversa_corazon * (np.linalg.det(esq_sup_izq) * np.linalg.det(esq_inf_derecha) - np.linalg.det(esq_inf_izq) * np.linalg.det(esq_sup_derecha))

M = np.array([[1, 2, 3], [4, 5, 4], [3, 2, 1]])
print(determinante_corazon(M))
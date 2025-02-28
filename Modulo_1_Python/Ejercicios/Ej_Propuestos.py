from typing import Tuple, Callable

def obtetener_funcion(P: Tuple[float, float], Q: Tuple[float, float])-> Callable[[float], float]:
    """
    Funcion que recibe dos puntos P y Q y devuelve la funcion de la recta que pasa por ellos.
    
    Parameters
    ----------
    P : Tuple[float, float]
        Punto P.
    Q : Tuple[float, float]
        Punto Q.

    Returns
    -------
    Callable[[float], float]
        Funcion de la recta que pasa por P y Q.

    Examples
    --------
    >>> P1 = (1, 2)
    >>> Q1 = (3, 4)
    >>> f1 = obtetener_funcion(P1, Q1)
    >>> f1(2)
    3.0
    """
    # Obtener pendiente
    m = (Q[1] - P[1]) / (Q[0] - P[0])
    # Obtener ordenada al origen
    b = P[1] - m * P[0]
    # Funcion de la recta
    return lambda x:  m * x + b
"""
P1 = (1, 2)
Q1 = (3, 4)
f1 = obtetener_funcion(P1, Q1)
print(f1(2))"""

# 5. Rotacion de Letras
def rotar_letra(letra: str, rotacion: int) -> str:
    """
    Funcion que recibe una letra y un numero y devuelve la letra rotada.
    
    Parameters
    ----------
    letra : str
        Letra a rotar.
    rotacion : int
        Numero de rotaciones.

    Returns
    -------
    str
        Letra rotada.

    Examples
    --------
    >>> rotar_letra('a', 1)
    'b'
    """

    inicio = ord('a') if letra.islower() else ord('A')

    return chr(inicio + (ord(letra) - inicio + rotacion) % 26)

"""print(rotar_letra('a', 1)) # b
print(rotar_letra('z', 1)) # a
print(rotar_letra('A', 1)) # B"""

# Hacer un diccionario enlazando Simbolo Rombo a 0, Pica a 1, Trebol a 2 y Corazon a 3
"""["♣♦♠", "♣♡"]  # Los dos números que se suman
suma = "♦♣♠"  # El resultado"""
def obtener_valor_simbolo():
    diccionario = {'♦': 0, '♠': 0, '♣': 0, '♡': 0}
    
    for rombo in range(10):  # Iteramos desde 0 hasta 9
        for pica in range(10):
            for trebol in range(10):
                for corazon in range(10):
                    suma1 = trebol * 100 + rombo * 10 + pica
                    suma2 = trebol * 10 + corazon
                    resultado_esperado = rombo * 100 + trebol * 10 + pica

                    if suma1 + suma2 == resultado_esperado and suma1 != suma2 != resultado_esperado:
                        return {'♦': rombo, '♠': pica, '♣': trebol, '♡': corazon}

    return -1  # No se encontró solución

# print(obtener_valor_simbolo())

# Conjuntos y diccionarios

el = {"correr", "saltar", "nadar", "caminar"}
ella = {"boxear", "nadar", "caminar", "saltar", "anda en bicicleta"}

# print(el & ella) #comunes
# print(el ^ ella) #unicas
# print(el | ella)
# print(ella - el)
# print(el - ella)

# MCD con conjuntos

def MCD(a, b):
    conj_a = {i for i in range(1, a + 1) if a % i == 0}
    conj_b = {i for i in range(1, b + 1) if b % i == 0}
    return max(conj_a & conj_b)
# print(MCD(5,10))

def texto_to_dicc(texto: str):
    lista_texto = texto.split("#")

    return {"telefono": lista_texto[0], "correo": lista_texto[1],\
               "direccion": lista_texto[2]}


print(texto_to_dicc("639232983 # blaky@ucm.es # calle BB 45 8-3-3 Madrid"))


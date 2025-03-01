# 1. a) MCD, generando las listas de divisores y seleccionando el mayor común. 


def MCD(a, b):
    def lista_divisores(numero):
        divisores = []
        for divisor in range(2,numero):
            if numero % divisor == 0:
                divisores.append(divisor)
        return divisores
    
    div_a = lista_divisores(a)
    div_b = lista_divisores(b)


    print(div_a, div_b)


    """divisores_comunes = []


    for divisor in div_a:
        if divisor in div_b:
            divisores_comunes.append(divisor)
    
    return max(divisores_comunes)"""


    return max([divisor for divisor in div_a if divisor in div_b])


#print(MCD(10,100))


"""
4. Tenemos una lista de enteros positivos y un número k. De cada fragmento
consecutivo de la lista con k elementos, consideramos su suma. ¿cuánto vale
la suma máxima? 
"""


def suma_maxima(lista, k):
    index = 0
    maximo = sum(lista[:k])


    """while index + k <= len(lista):
        maximo = sum(lista[index : index + k]) if sum(lista[index : index + k]) > maximo else maximo
        index += 1


    return maximo"""


    maximo = max(sum(lista[index:index+k]) for index in range(len(lista) -k + 1))
    return maximo


#print(suma_maxima([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4))


# Si es muy grande, hacerlo mas efectivo:
def suma_maxima_efectiva(lista, k):
    index = 0
    maximo = sum(lista[:k])
    suma_actual = maximo


    # while index + k <= len(lista) - k:
    for index in range(len(lista) - k):
        suma_actual = suma_actual - lista[index] + lista[index + k]
        maximo = suma_actual if suma_actual > maximo else maximo
            


    return maximo


# print(suma_maxima_efectiva([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4))


def criba_erastotenes(n: int):
    lista = list(range(n + 1)) # Lista de 1 hasta n incluido, len = n+1
    i = 2


    while i < len(lista):
        primo = lista[i]
        i += 1
        j = i
        while j < len(lista):
            if lista[j] % primo == 0:
                lista.pop(j)
            j += 1


    return lista


#print(criba_erastotenes(100))
def derivada_n_esima(coeficientes, n = 1):
    def derivada_de_polinomio(indices):
        indices_derivada = []


        for i, coeficiente in enumerate(indices):
            indices_derivada.append(i * coeficiente)


        return indices_derivada[1:]
    
    coeficientes_derivada = coeficientes


    for _ in range(n):
        coeficientes_derivada = derivada_de_polinomio(coeficientes_derivada)
    
    return coeficientes_derivada


# print(derivada_n_esima([3, 4, 5], 1))  # Salida: [4, 10]
# print(derivada_n_esima([2, 0, 4, 9], 2))  # Salida: [24]
# print(derivada_n_esima([5, 3, 0, 1], 3))  # Salida: [6]
# print(derivada_n_esima([1, 0, 0, 4, 3]))  # Salida: [0, 0, 12, 12]
# print(derivada_n_esima([10, 5], 1))  # Salida: [5]


"""
7. Python proporciona distintas maneras de ordenar una lista. Nos interesa
especialmente poder hacerlo usando una función arbitraria que compare los
elementos.
Tenemos una colección de puntos del plano, esto es, una lista de pares de
reales. La llamamos, sencillamente “puntos”.
a) Para hacer los siguientes apartados, crea una lista de puntos del plano
restringida a −10 ≤ 𝑥 ≤ 10, −10 ≤ 𝑦 ≤ 10, esto es, (𝑥, 𝑦) ∈ [−10, 10)ଶ
"""
from collections import defaultdict
import random
import math
import cmath


def lista_puntos_ordenada():
    lista_puntos = []
    for _ in range(10):
        lista_puntos.append((random.randint(-10, 10), random.randint(-10, 10)))


    def distancia_punto_origen(punto_a):
        return math.sqrt(punto_a[0]**2 + punto_a[1]**2)
    
    def distancia_punto_punto(Punto_referencia, punto_a):
        return math.sqrt((punto_a[0] - Punto_referencia[0])**2 + (punto_a[1] - Punto_referencia[1])**2)


    # lista_puntos.sort(key=distancia_punto_origen)
    lista_puntos.sort(key=lambda punto: distancia_punto_punto([0, 0], punto))


    return lista_puntos


# print(lista_puntos_ordenada())


"""
lista_puntos.sort(key=lambda punto: distancia_punto_punto([0, 0], punto))
Aquí estamos ordenando lista_puntos usando la función sort con la clave key. 
La clave define el criterio por el cual se ordenarán los elementos de la lista.


lambda: Es una función anónima que creamos en el momento, sin necesidad de definirla previamente. 
En este caso, lambda punto: distancia_punto_punto([0, 0], punto) es equivalente a:


python
def distancia_desde_origen(punto):
    return distancia_punto_punto([0, 0], punto)
Paso de Parámetros: lambda punto: distancia_punto_punto([0, 0], punto) toma cada punto de lista_puntos,
lo pasa a distancia_punto_punto junto con el punto de referencia 
[0,0], y devuelve la distancia que se usa para ordenar los puntos.


El motivo por el cual no puedes usar directamente sort(key=distancia_punto_punto([0, 0])) es que distancia_punto_punto([0, 0])
no devolvería una función, sino el resultado de intentar calcular una distancia, lo cual no tendría sentido en este contexto.
lambda permite crear una pequeña función en línea que se ajusta perfectamente a lo que sort necesita para ordenar los elementos
"""


def cambiar_vocales_a_punto(texto):
    texto_nuevo = ""
    for letra in texto:
        texto_nuevo += letra if letra not in "aeiouAEIOU" else "."
    
    return texto_nuevo


    #return "".join([letra if letra not in "aeiouAEIOU" else "." for letra in texto])


# print(cambiar_vocales_a_punto("Hola que tal estAs"))


def contabilizar_items(items):
    diccionario = {}


    for item in items:
        if item in diccionario:
            diccionario[item] += 1
        else:
            diccionario[item] = 1
            
    
    print(diccionario)


# contabilizar_items("aeioua")


"""
from collections import defaultdict


# Inicialización del diccionario con valor por defecto
contador = defaultdict(int)


# Lista de elementos para contar
elementos = ['manzana', 'banana', 'manzana', 'pera', 'banana', 'manzana']


# Contar las apariciones de cada elemento
for elemento in elementos:
    contador[elemento] += 1


# Mostrar el resultado
print(dict(contador))"""

def prueba_memoria():
    listaA = [1, 2, 3]
    listaB = listaA

    listaA[0] = 0

    print(listaA, listaB) # Ambas Cambian



# prueba_memoria()

"""
ARCHIVOS
"""

# 2.
def leer_archivo_y_enumerarlo(archivo):
    with open(archivo, 'r') as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            print(i," ", line.strip())

        # Contar palabras en linea
        n_palabras = 0
        for line in lines:
            n_palabras += len(line.split())
        print("Media palabras ", n_palabras/len(lines))


# leer_archivo_y_enumerarlo("texto.txt")

# En diccionario
def leer_archivo_diccionario(archivo):
    with open(archivo, 'r') as f:
        lines = f.read()

        # palabras = []
        # [palabras.append(palabra) for palabra in set(lines.split())]

        palabras = defaultdict(int)
        for palabra in lines.split():
            palabras[palabra] += 1
        
        p2 = defaultdict(set)
        for pal, freq in palabras.items():
            p2[freq].add(pal)

        print(p2)


# leer_archivo_diccionario("texto.txt")

# Objetos Mutables e Inmutables
"""
Si quisieramos modificar un entero (inmutable) dentro de una función,
no podríamos hacerlo directamente, ya que los argumentos de las funciones en Python son pasados por valor.
Sin embargo, si el entero estuviera dentro de una lista (mutable), podríamos modificarlo sin problemas.

Se podría pasar tambien dentro de un objeto mutable, como una lista, y modificarlo dentro de la función.
"""
def modificar_entero(numero)->int:
    numero += 1
    return numero

x = 10
x = modificar_entero(x)
# print(x) # Salida: 11

"""
Una fracción se puede simplificar calculando el máximo común divisor de sus
términos… Diseña una función que da la fracción simplificada y otro que
simplifica “in place” una fracción dada.
"""
def simplificar_fraccion(numerador, denominador):
    def MCD(a, b):
        while b != 0: 
            a, b = b, a % b
        return a


    mcd = MCD(numerador, denominador)
    return numerador // mcd, denominador // mcd
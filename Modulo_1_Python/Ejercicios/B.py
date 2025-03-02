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

# Exccepciones 3

"""
Los valores missing se tratan con frecuencia mediante el uso de excepciones.
Supongamos que las calificaciones de alguien son las siguientes:
notas = “2,,5,7,12,None,-3”
(La segunda nota es inexistente; otra es None; otra, negativa o podría ser
mayor que 10.)
Tras separar las notas, deseamos convertirlas con las función float. Pero
cuando falle esta conversión (por tratarse de un dato inexistente o por tener
el valor None u otro string no convertible en un real), deseamos imputar un
cero. Cuando sea negativa, también un cero; y cuando sea mayor que 10, lo
dejaremos en 10."""

def tratar_notas(notas):
    def tratar_nota(nota):
        try:
            nota = float(nota)
            if nota < 0:
                raise ValueError
            elif nota > 10:
                return 10
        except:
            return 0
        return nota


    notas = notas.split(",")
    notas = [tratar_nota(nota) for nota in notas]
    return sum(notas)/len(notas)

class complejo():
    def __init__(self, modo = "binomico", x_t = 0, y_t = 0):
        self.modo = modo
        self.x = x_t
        self.y = y_t
        self.r = math.sqrt(self.x**2 + self.y**2)

        if self.x != 0:
            self.titus = math.atan(self.y/self.x) 
        elif self.y > 0:
            self.titus = math.pi / 2
        elif self.y < 0:
            self.titus = math.pi / 2 * -1
        else:
            self.titus = None


    
    def __str__(self):
        if self.modo == "binomico":
            return ("{} + {}i".format(self.x, self.y))
        elif self.modo == "polar":
            return ("{} * e^({}i)".format(self.r, self.titus))
    
    def __add__(self, other): # Suma +
        return complejo("binomico", self.x + other.x, self.y + other.y)

    def __sub__(self, other):# Resta -
        return complejo("binomico", self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return complejo("polar", self.r * other.r, self.titus + other.titus)
    def __truediv__(self, other):
        return complejo("polar", self.r / other.r, self.titus - other.titus)
    def __pow__(self, other):
        return complejo("polar", self.r ** other.r, self.titus * other.titus)
    def __abs__(self):
        return self.r
    def __neg__(self): # Negativo unario -x
        return complejo("binomico", -self.x, -self.y)
    def __eq__(self, other): # Igualdad ==
        return self.x == other.x and self.y == other.y
    def __ne__(self, other): # Diferente !=
        return not self == other
    def __lt__(self, other): # Menor que <
        return self.r < other.r
    def __le__(self, other): # Menor o igual que <=
        return self.r <= other.r
    def __gt__(self, other): # Mayor que >
        return self.r > other.r
    def __ge__(self, other): # Mayor o igual que >=
        return self.r >= other.r

# punto = complejo("polar", 2, 3)
# print(punto)

class Ficha_Persona():
    def __init__(self, nom = "", f_nacimiento = "00/00/000", edad = 0, estatura = 0, aficciones = [], email = "@"):
        self.nombre = nom
        self.fecha_nacimiento = f_nacimiento
        self.edad = edad
        self.estatura = estatura
        self.aficiones = aficciones
        self.email = email

        datos = [self.nombre, self.fecha_nacimiento, self.edad, self.estatura, self.aficiones]

        self.diccionario = {self.email : datos}

    def __str__(self):
        return str(self.diccionario)

persona = Ficha_Persona()
# print(persona)

"""
PF Y ORDEN SUPERIOR
"""

"""
1. - La lista con los cuadrados de los 100 primeros números
- Ídem, pero únicamente de los números pares.
"""

def es_primo(numero):
    if numero < 2:
        return False
    for i in range(2, numero):
        if numero % i == 0:
            return False
    return True

lista_primos = filter(es_primo, range(100))

lista_primos_cuadrado = list(map(lambda x: x**2, lista_primos))

# print(list(lista_primos_cuadrado))

"""
2. (*) Diseña funciones para los siguientes cálculos:
- La derivada de una función (derivable) en un punto
- El método de bipartición para calcular el cero de una función en un
intervalo supuesto que...
- Newton-Raphson, partiendo de un punto y supuesto que...
b- Dado el término general de una sucesión 𝑎􀯡 de reales (que en realidad es
una función 𝑎 ∶ 𝑁 → 𝑅), define la función que da la lista de términos 𝑎􀯜
para 𝑖 ∈ {𝑎􀬵, … , 𝑎􀯡}, aplicando la función a cada término de la lista [1, …,
n] mediante la función map.
- Expresa la función “sumatorio”, que suma los términos de una sucesión
entre dos límites dados, esto es, usando lambda expresiones.

"""

def derivada_punto(F, a):
    def derivada(F):
        h = 1e-5
        return lambda x: (F(x + h) - F(x))/h
        
    return derivada(F)(a)

# print(derivada_punto(lambda x: x**2, 5))
#b
def a(i):
    return i**2

lista = [0, 1, 2, 3, 4, 5, 6]

# print(list(map(a, lista)))

# Sumatorio

from functools import reduce
def sumatorio(a, b):
    def suma(x, y):
        return x+y

    return reduce(suma, range(a, b + 1))
    
# print(sumatorio(1, 3))

# fun = lambda a, b: lambda c : (a(b(c)), b(a(c)))
"""
La funcion fun toma dos funciones a y b, y devuelve una nueva función que toma un argumento c 
y devuelve una tupla con el resultado de aplicar a a b(c) y b a c.

"""

# La función máximo se puede definir mediante un reduce:
def maximo(lista):
    def mx(a, b):
        return a if a>= b else b
    #return reduce(mx, lista)

    return reduce(lambda x, y: x if x >= y else y, lista)

# print(maximo([1, 2, 3, 600, 4]))

"""6. Dada una lista de nombres de persona, tenemos una función que selecciona
los que tienen una longitud menor o igual a una cantidad, dada."""

nombres = ["pedro", "juan", "maria", "Ana", "luis", "carlos", "josefina", "luisa", "luisito", "luisito2"]

sort_names = lambda nombres, longitud : list(filter(lambda nombre: True if len(nombre) <= longitud else False, nombres))

# print(list(sort_names(nombres, 3)))

"""7. Define la función select_multiplos(n, k), que genera los números desde 1
hasta n que son múltiplos de k. Hazlo usando listas por comprensión."""

def select_multiplos(n, k):
    return [i for i in range(1, n + 1) if i%k == 0]

# print(select_multiplos(10, 2))

# Imprimir primos
# print([i for i in range(2, 100) if es_primo(i)])

"""(*) Genera una lista con 25 pares de enteros aleatorios, entre 1 y 10: son las
coordenadas de 25 puntos del plano discreto. Almacenamos esta lista en una
variable lista_inicial, y en otra lista_de_trabajo, con la que vamos a trabajar.
Ahora, define una función que reciba dos puntos del plano discreto (dos
pares de enteros) y calcule la distancia euclídea entre dichos puntos.
Define ahora una función de orden superior tal que, dado un punto 𝑃, dé la
función 𝑑𝑖𝑠𝑡􀯉, que calcula la distancia (a 𝑃) de un punto: 𝑑𝑖𝑠𝑡􀯉(𝑄) = ‖􀴤𝑃􀴤􀴤𝑄􀴤‖.
Define una función que, dado un punto y una lista de puntos, devuelve la
lista de puntos dada, pero ordenada de menor a mayor distancia a 𝑃."""

lista_inicial = [((random.randint(1, 10), random.randint(1, 10))) for _ in range(26)]

def distancia_euclidea(punto_a, punto_b):
    return math.sqrt((punto_a[0] - punto_b[0])**2 + (punto_a[1] - punto_b[1])**2)

lista_trabajo = lista_inicial.copy()

def distancia_punto(P):
    return lambda Q: math.sqrt((P[0] - Q[0])**2 + (P[1] - Q[1])**2)

def puntos_ordenados(Punto, ListaPuntos):
    return list(sorted(ListaPuntos, key = distancia_punto(Punto)))

def puntos_ordenados_diccionario(Punto, ListaPuntos):
    d = {punto: distancia_punto(Punto)(punto) for punto in ListaPuntos}


    return d

lista = [(0,0), (1,0), (1, 1), (-1, 0)]

# print(puntos_ordenados_diccionario((0,0), lista))
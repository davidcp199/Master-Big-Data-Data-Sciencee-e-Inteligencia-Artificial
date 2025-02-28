def descomposicion_en_factores(numero: int)->int:
    divisor = 2
    contador = 0
    resto = numero


    while resto > 1 and divisor <= resto:
        while resto % divisor == 0:
            print("{}|{}".format(resto,divisor))
            resto //= divisor
        contador = 0
        divisor += 1
    print("{}|".format(resto))


def cambio_monedas(dinero: int):
    assert type(dinero) == int


    monedas = [25, 5, 1]
    cambio = [0, 0, 0]
    resto = dinero


    for i, moneda in enumerate(monedas):
        if resto >= moneda:
            cambio[i] = resto // moneda
            resto %= moneda
                
    print(cambio)


#cambio_monedas(101)


"""
Si tenemos los coeficientes (𝑎, 𝑏, 𝑐) de una ecuación de segundo grado de la
forma 𝑎𝑥**2 + 𝑏𝑥 + 𝑐 = 0 y suponiendo que tiene dos raíces reales, expresa
instrucciones para calcular dichas fórmulas. 


SOL
    (-b +- rs(b**2-4*a*c)) / 2a


"""
import math
import cmath


def polinomio(a, b, c):
    return (-b + cmath.sqrt(b**2 - 4 * a * c)) / 2 * a, (-b - cmath.sqrt(b**2 - 4 * a * c)) / 2 * a


#print(polinomio(1,4,3))


import random


def biparticion(funcion: callable, a:float, b: float, tolerancia: float = 1e-100000000000):
    while (b - a) / 2 > tolerancia:
        c = (a + b) / 2
        if funcion(c) == 0:
            print(f(c))
            return c
        elif funcion(a) * funcion(c) < 0:
            b = c
        else:
            a = c
    print(f((a + b) / 2))
    return (a + b) / 2


f = lambda x: x**2 - 5*x + 6


#print(biparticion(f, 2, 3))


def filtrar_minusculas(texto: str):
    lista = texto.split(" ")
    lista_minuscula = []


    for palabra in lista:
        lista_minuscula.append(palabra) if palabra.islower() else None


    print(lista_minuscula)


filtrar_minusculas("Hola me llamo David")
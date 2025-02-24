# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 17:05:37 2021

@author: cpareja
"""
import random

Colores = {"Azul": 3.0, "Blanco": 5.0, "Verde": 15.0, "Amarillo": 10.0}

def v_a(color):
    return random.random() * 2 + Colores[color] - 1

def generar_datos(archivo, n):
    with open(archivo, "w") as f:
        for _ in range(n):
            [color] = random.choices(list(Colores.keys()))
            x = round(v_a(color), 2)
            f.write(color + " " + str(x) + "\n")
                
    
#!/usr/bin/python
# -*- coding: utf-8 -*-

# A1 - magia - solución - B

"""
@autor: C. Pareja Flores
@titulo: ¡Magia! (ejecutable desde el prompt del s.o.)
"""

def main():
    print("Empieza el juego")
    print("Para este truco, vas a necesitar un dado.", end="")
    input("y si no lo tienes, invéntate los resultados...            <enter>")
    
    print("Lanza el dado y fíjate en el resultado.", end="")
    input("(Supongamos que obtienes un 4)                            <enter>")
    
    print("Multiplícalo por 2 y suma 5 al resultado...")
    print("... Tenemos 4 × 2 = 8; 8 + 5 = 13", end="")
    input("Multiplica lo que tienes ahora por 5... 13 × 5 = 65       <enter>")
    
    print("Y ahora, lanza el dado de nuevo...", end="")
    print("... Supongamos que obtienes un 3...", end="")
    input("... y añade la puntuación obtenida al resultado anterior. <enter>")
    
    entrada = input("Ahora dime el resultado obtenido: ")
    n = int(entrada)
    a, b = (n-25) // 10, (n-25) % 10
    
    print("Ahora adivinaré los números de los dados.", end="")
    input("Déjame pensar...                                         <enter>")
    
    print("Los números de los dados fueron " + str(a) + " y " + str(b) + ".")
    print("Hasta otra.")

if __name__ == '__main__':
    main()

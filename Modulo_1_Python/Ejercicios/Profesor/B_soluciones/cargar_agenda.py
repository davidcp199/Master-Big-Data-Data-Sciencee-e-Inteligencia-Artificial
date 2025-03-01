# -*- coding: utf-8 -*-
"""
@author: CPAREJA
"""

import sys

def cargar_agenda(nombre_archivo):
    agenda = dict({})
    el_archivo = open(nombre_archivo, "r")
    for l in el_archivo:
        datos = l.split(" # ")
        agenda[datos[0]] = {
            "email" : datos[1],
            "direc" : datos[2].rstrip()
        }
    el_archivo.close()
    return agenda

def listado(agenda):
    print("telefono   email             direccion")
    print("---------- ---------------   -----------------------------")
    for telefono, datos in agenda.items():
        print(telefono.ljust(10), 
              datos["email"].ljust(17),
              datos["direc"])

def main():
    if len(sys.argv) != 2:
        print ('uso correcto: python ./programa.py' \
            + '<nombre archivo agenda>')
        sys.exit(1)

    nombre_archivo = sys.argv[1]
    try:
        agenda = cargar_agenda(nombre_archivo)
        listado(agenda)   
    except:
        print("No hemos podido cargar la agenda")
        print("Comprueba su nombre, ruta y formato.")

if __name__ == '__main__':
    main()

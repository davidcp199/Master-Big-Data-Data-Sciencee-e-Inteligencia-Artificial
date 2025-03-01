from complejoBin import *
from math import pi

z1 = Complejo("binom", 4, 3)
print(z1)
z1.escribir_complejo_binom()
z1.escribir_complejo_polar()
print(z1.parte_real(), z1.parte_imag(), z1.modulo(), z1.argumento())

print()

z2 = Complejo("polar", 5, pi/6)
z2.escribir_complejo_binom()
z3 = z1 + z2
z3.escribir_complejo_binom()
   

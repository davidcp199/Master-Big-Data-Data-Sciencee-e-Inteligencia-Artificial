from math import sin, cos, sqrt, atan

class Complejo:
    """Clase Complejo, basada en su representación binómica"""

    componente_real = None
    componente_imag = None

    def __init__(self, modo, real_o_radio, imag_o_argumento):
        if modo == "binom":
            self.componente_real = real_o_radio
            self.componente_imag = imag_o_argumento
        if modo == "polar":
           self.componente_real = real_o_radio * cos(imag_o_argumento)
           self.componente_imag = real_o_radio * sin(imag_o_argumento)

    def parte_real(self):
        return self.componente_real

    def parte_imag(self):
        return self.componente_imag
        
    def modulo(self):
        return sqrt(self.componente_real ** 2 + self.componente_imag ** 2)

    def argumento(self):
        return atan(self.componente_real / self.componente_imag)

    def escribir_complejo_binom(self):
        print("[" + str(self.componente_real)
              + ", " + str(self.componente_imag) + "]")

    def escribir_complejo_polar(self):
        print("<" + str(self.modulo())
              + ", " + str(self.argumento()) + ">")

    def __add__(self, other):
        parte_real_nueva = self.componente_real + other.parte_real()
        parte_imag_nueva = self.componente_imag + other.parte_imag()
        return Complejo("binom", parte_real_nueva, parte_imag_nueva)

"""
Las demás operaciones también pueden sobrecargarse:
https://www.programiz.com/python-programming/operator-overloading
"""

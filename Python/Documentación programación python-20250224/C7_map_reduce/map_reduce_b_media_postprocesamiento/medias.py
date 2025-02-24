import sys
from mrjob.job import MRJob

def suma_doble(pares):
    """Ej. [(1, 10), (2, 20), (3, 30)]  --> (6, 60)"""
    a, b = 0, 0
    for x, y in pares:
        a, b = a + x, b + y
    return a, b

class MRSumaTotales(MRJob):
   
    def mapper(self, _, linea):
        [color, x] = linea.split()
        yield color, (float(x), 1)
              
    def reducer(self, key, values):
        yield key, suma_doble(values)
        
if __name__ == '__main__':
    archivo_datos = sys.argv[1]
    trabajo = MRSumaTotales(args=[archivo_datos])    
    with trabajo.make_runner() as runner:
        runner.run()
        for key, value in trabajo.parse_output(runner.cat_output()):
            media = value[0] / value[1]
            media_str = str(round(media, 2))
            print(key + " - " + media_str)





def sumatorio(n):
    acum = 0
    for i in range(n):
        acum = acum + i**2/(i+1)
    return suma
        

def polinomio(n, x):
    acum = 0
    for i in range(1, n+1):
        acum = acum*x + i
    return suma

import sys
from mrjob.job import MRJob

class MRLanguageBudgetCountries(MRJob):
    def mapper(self, _, linea):
        campos = linea.split('|')
        
        if len(campos) == 5:
            titulo, ano, idioma, pais, presupuesto = campos
            
            if idioma and pais and presupuesto != '-1' and presupuesto != '' and pais != '':
                try:
                    presupuesto = float(presupuesto)
                    yield idioma, (pais, presupuesto)
                except ValueError:
                    pass
    def reducer(self, key, values):
        paises_presupuestos = {}

        for pais, presupuesto in values:
            if pais not in paises_presupuestos:
                paises_presupuestos[pais] = 0
            paises_presupuestos[pais] += presupuesto
        
        for pais, total_presupuesto in paises_presupuestos.items():
            yield key, (pais, total_presupuesto)

if __name__ == '__main__':
    MRLanguageBudgetCountries.run()

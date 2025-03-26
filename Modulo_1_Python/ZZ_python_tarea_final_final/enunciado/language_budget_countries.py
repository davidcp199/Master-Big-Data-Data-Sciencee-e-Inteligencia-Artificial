import sys
from mrjob.job import MRJob

class MRLanguageBudgetCountries(MRJob):
    """
    MapReduce job que calcula el presupuesto total por país para cada idioma en los datos de películas.

    Cada línea del archivo de entrada debe tener el siguiente formato:
        "título|año|idioma|país|presupuesto"
    
    Se ignoran líneas que no cumplan con el formato o que tengan datos no válidos.
    """
    def mapper(self, _, linea):
        """
        Procesa una línea de entrada y emite tuplas (idioma, (país, presupuesto)).

        Parameters
        ----------
        _ : any
            Clave no utilizada.
        linea : str
            Línea de texto que contiene los datos de una película en el formato:
            "título|año|idioma|país|presupuesto".
        
        Yields
        ------
        tuple
            Clave-valor de la forma (idioma, (país, presupuesto)).

        Examples
        --------
        >>> list(MRLanguageBudgetCountries().mapper(None, "Pelicula|2020|Español|España|1000000"))
        [('Español', ('España', 1000000.0))]
        """
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
        """
        Agrega los presupuestos por país para un idioma dado.

        Parameters
        ----------
        key : str
            Idioma (clave del grupo).
        values : iterable
            Iterable de tuplas (país, presupuesto) asociadas a un idioma.
        
        Yields
        ------
        tuple
            Clave-valor en la forma (idioma, (país, presupuesto_total)) donde presupuesto_total es la suma de presupuestos
            de ese país para el idioma especificado.

        Examples
        --------
        >>> list(MRLanguageBudgetCountries().reducer("Español", [("España", 1000000.0), ("España", 500000.0)]))
        [('Español', ('España', 1500000.0))]
        """
        paises_presupuestos = {}

        for pais, presupuesto in values:
            if pais not in paises_presupuestos:
                paises_presupuestos[pais] = 0
            paises_presupuestos[pais] += presupuesto
        
        for pais, total_presupuesto in paises_presupuestos.items():
            yield key, (pais, total_presupuesto)

if __name__ == '__main__':
    MRLanguageBudgetCountries.run()
